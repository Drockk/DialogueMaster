#pragma once

#include <common.h>
#include <llama.h>

namespace dm {
class DialogueMaster {
public:
    ~DialogueMaster();

    void loadModel(const std::string& t_modelPath, float t_minP, float t_temperature);
    void addChatMessage(const std::string& t_message, const std::string& t_role);
    void startCompletion(const std::string& t_query);

    std::string completionLoop();
    void stopCompletion();

private:
    llama_context* m_ctx;
    llama_model* m_model;
    llama_sampler* m_sampler;
    llama_batch m_batch;
    llama_token m_currToken;

    std::vector<llama_chat_message> m_messages{};
    std::vector<char> m_formattedMessages{};
    std::vector<llama_token> m_promptTokens{};
    int m_previousLength{0};
    std::string m_response{};
};
} // namespace dm