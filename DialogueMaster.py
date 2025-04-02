from vllm import LLM, EngineArgs
from vllm.utils import FlexibleArgumentParser

def main(args: dict):
    # Pop arguments not used by LLM
    max_tokens = args.pop("max_tokens")
    temperature = args.pop("temperature")
    top_p = args.pop("top_p")
    top_k = args.pop("top_k")
    chat_template_path = args.pop("chat_template_path")

    # Create an LLM
    llm = LLM(**args)

if __name__ == "__main__":
    parser = FlexibleArgumentParser()

    # Add engine args
    engine_group = parser.add_argument_group("Engine arguments")
    EngineArgs.add_cli_args(engine_group)
    engine_group.set_defaults(model="meta-llama/Llama-3.2-1B-Instruct")
    