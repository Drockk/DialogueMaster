#include "llama.h"

#include <array>
#include <iostream>
#include <string>
#include <vector>

int main() {
    using namespace std::string_literals;

    ggml_backend_load_all();

    const auto ngl = 99;
    const auto nPredict = 32;

    auto modelParams = llama_model_default_params();
    modelParams.n_gpu_layers = ngl;

    const auto modelPath = "models/ggml-model-f16.gguf";
    auto* model = llama_model_load_from_file(modelPath, modelParams);
    const auto* vocab = llama_model_get_vocab(model);

    if (model == nullptr) {
        std::cerr << "Failed to load model from file: " << modelPath << std::endl;
        return 1;
    }

    const auto prompt = "Are you happy?"s;
    const auto nPrompt = -llama_tokenize(vocab, prompt.c_str(), prompt.size(), NULL, 0, true, true);

    std::vector<llama_token> promptTokens(nPrompt);
    if (llama_tokenize(vocab, prompt.c_str(), prompt.size(), promptTokens.data(), promptTokens.size(), true, true) < 0) {
        std::cerr << "Failed to tokenize the prompt" << std::endl;
        return 1;
    }

    auto ctxParams = llama_context_default_params();
    ctxParams.n_ctx = nPrompt + nPredict - 1;
    ctxParams.n_batch = nPrompt;
    ctxParams.no_perf = false;

    auto* ctx = llama_init_from_model(model, ctxParams);
    if (ctx == nullptr) {
        std::cerr << "Failed to create the llama_context" << std::endl;
        return 1;
    }

    auto sparams = llama_sampler_chain_default_params();
    sparams.no_perf = false;
    auto* smpl = llama_sampler_chain_init(sparams);

    llama_sampler_chain_add(smpl, llama_sampler_init_greedy());

    for (auto id : promptTokens) {
        std::array<char, 128> buffer{};
        const auto n = llama_token_to_piece(vocab, id, buffer.data(), buffer.size(), 0, true);

        if (n < 0) {
            std::cerr << "Failed to convert token to piece" << std::endl;
            return 1;
        }

        std::string piece(buffer.data(), n);
        std::cerr << piece << " ";
    }

    auto batch = llama_batch_get_one(promptTokens.data(), promptTokens.size());

    const auto t_main_start = ggml_time_us();
    int n_decode = 0;
    llama_token new_token_id;

    for (int n_pos = 0; n_pos + batch.n_tokens < nPrompt + nPredict; ) {
        // evaluate the current batch with the transformer model
        if (llama_decode(ctx, batch)) {
            fprintf(stderr, "%s : failed to eval, return code %d\n", __func__, 1);
            return 1;
        }

        n_pos += batch.n_tokens;

        // sample the next token
        {
            new_token_id = llama_sampler_sample(smpl, ctx, -1);

            // is it an end of generation?
            if (llama_vocab_is_eog(vocab, new_token_id)) {
                break;
            }

            char buf[128];
            int n = llama_token_to_piece(vocab, new_token_id, buf, sizeof(buf), 0, true);
            if (n < 0) {
                fprintf(stderr, "%s: error: failed to convert token to piece\n", __func__);
                return 1;
            }
            std::string s(buf, n);
            printf("%s", s.c_str());
            fflush(stdout);

            // prepare the next batch with the sampled token
            batch = llama_batch_get_one(&new_token_id, 1);

            n_decode += 1;
        }
    }

    std::cerr << "\n";
    llama_perf_sampler_print(smpl);
    llama_perf_context_print(ctx);
    std::cerr << "\n";

    //Destruction
    llama_sampler_free(smpl);
    llama_free(ctx);
    llama_model_free(model);

    return 0;
}
