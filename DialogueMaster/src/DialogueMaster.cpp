#include "DialogueMaster.hpp"

#include <chat.h>
#include <iostream>

namespace dm {
DialogueMaster::~DialogueMaster() {
    for (auto& message: m_messages) {
        delete message.content;
    }

    llama_kv_cache_clear(m_ctx);
    llama_sampler_free(m_sampler);
    llama_free(m_ctx);
    llama_model_free(m_model);
}

void DialogueMaster::loadModel(const std::string& t_modelPath, float t_minP, float t_temperature) {
    // Create instance of llama_model
    auto modelParams = llama_model_default_params();

    m_model = llama_model_load_from_file(t_modelPath.c_str(), modelParams);
    if (m_model == nullptr) {
        throw std::runtime_error("Failed to load model from file: " + t_modelPath);
    }

    // Create instance of llama_context
    auto ctxParams = llama_context_default_params();
    ctxParams.n_ctx = 0;
    ctxParams.no_perf = true;

    m_ctx = llama_new_context_with_model(m_model, ctxParams);
    if (m_ctx == nullptr) {
        throw std::runtime_error("Failed to create the llama_context");
    }

    // Initialize sampler
    auto samplerParams = llama_sampler_chain_default_params();
    samplerParams.no_perf = true;

    m_sampler = llama_sampler_chain_init(samplerParams);
    llama_sampler_chain_add(m_sampler, llama_sampler_init_min_p(t_minP, 1));
    llama_sampler_chain_add(m_sampler, llama_sampler_init_temp(t_temperature));
    llama_sampler_chain_add(m_sampler, llama_sampler_init_dist(LLAMA_DEFAULT_SEED));

    m_formattedMessages = std::vector<char>(llama_n_ctx(m_ctx));
    m_messages.clear();
}

void DialogueMaster::addChatMessage(const std::string& message, const std::string& role) {
    m_messages.push_back({ strdup(role.c_str()), strdup(message.c_str()) });
}

void DialogueMaster::startCompletion(const std::string& query) {
    addChatMessage(query, "user");

    // Apply the chat-template
    const auto* tmpl = llama_model_chat_template(m_model, nullptr);
    auto newLength = llama_chat_apply_template(
        tmpl,
        m_messages.data(),
        m_messages.size(),
        true,
        m_formattedMessages.data(),
        m_formattedMessages.size()
    );

    if (newLength > static_cast<int>(m_formattedMessages.size())) {
        m_formattedMessages.resize(newLength);
        newLength = llama_chat_apply_template(tmpl, m_messages.data(), m_messages.size(), true, m_formattedMessages.data(), m_formattedMessages.size());
    }

    if (newLength < 0) {
        throw std::runtime_error("Failed to apply chat template");
    }

    std::string prompt(m_formattedMessages.begin() + m_previousLength, m_formattedMessages.begin() + newLength);
    m_promptTokens = common_tokenize(m_ctx, prompt, true, true);

    m_batch.token = m_promptTokens.data();
    m_batch.n_tokens = m_promptTokens.size();
}

std::string DialogueMaster::completionLoop() {
    int contextSize = llama_n_ctx(m_ctx);
    int nCtxUsed = llama_get_kv_cache_used_cells(m_ctx);
    if (nCtxUsed + m_batch.n_tokens > contextSize) {
        std::cerr << "context size exceeded" << '\n';
        exit(0);
    }

    if (llama_decode(m_ctx, m_batch) < 0) {
        throw std::runtime_error("llama_decode() failed");
    }

    m_currToken = llama_sampler_sample(m_sampler, m_ctx, -1);
    if (llama_token_is_eog(m_model, m_currToken)) {
        addChatMessage(strdup(m_response.data()), "assistant");
        m_response.clear();
        return "[EOG]";
    }
    std::string piece = common_token_to_piece(m_ctx, m_currToken, true);

    m_batch.token = &m_currToken;
    m_batch.n_tokens = 1;

    return piece;
}
} // namespace dm
