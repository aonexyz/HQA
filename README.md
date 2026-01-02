# H Q A

H Q A is a command line tool to level up codebases to `HQA` (high quality using AI) (local by default). It processes files in a specified directory, creates backups, and applies AI-based improvements to enhance code quality.

## Installation
Recommended: Install using `pipx`:
```bash
pipx install git+https://github.com/aonexyz/HQA
```

Install using pip:

```bash
pip install git+https://github.com/aonexyz/HQA
```
<PyPI coming soon>

## Simple Example
```bash
HQA <folder> <file-extension>
```

For example:

```bash
HQA ./src dart
```
This command processes all Dart files in the `./src` directory, creates a backup, and applies AI-based improvements using the default model and API.

By default, it assumes the name of the language (as used in Markdown code blocks) is the same as the file extension, in other languages, such as python and JavaScript, you need to specify the language name using `-n <name>` (e.g., `h1-code src py -n python`)

### OpenAI
by default it assumes you have an [Ollama](https://github.com/ollama/ollama) server, with the model of `llama3.1`.
You can change the model using `--model` option, the URL (for example, to ClosedAI) with `--base_url` option, and api-key using `--api_key`.

## HQA code quality.
H1 code quality defines what clean and clear code means, as understood by an LLM, according to my perspective. You can find the exact system prompt in the [`ai.py`](https://github.com/aonexyz/HQA/blob/main/HQA/ai.py#L4) file, but the main points are:

* No redundant or duplicate code.
* Comments should be useful and non-trivial. Without commented-out code.
* limited hallucinations - the AI should not try to explain things it don't understand.
* minimal documentation (by default, see [documentation-level](#Documentation-level) section) - it should create minimal explanation when needed. 
* if really needed, and it won't break your code, changing names for clarity.
* Follow the recommended syntax and conventions of the language.

> Note: by its very nature, the Converter to H1 doesn't always result in valid code, so make sure you check the files after the convert with an IDE to see if there are errors.

## Documentation-level
you can use choose the documentation level use `-lvl <0-4>` or `--doc-level <0-4>`:
-   0. No docstring or documentation for functions at all, but still try to explain in comments when absolutely needed.
-   1. (the default) Very minimal documentation, ideally one line or less.
-   2. Minimal documentation, brief overview in 2–3 sentences, focusing on key points.
-   3. Moderate documentation, providing some explanations and key details, but avoiding unnecessary depth.
-   4. Detailed documentation, including explanations, use cases, and examples.

### Documentation-only
you can use the option `--doc` to Only write documentation, without improving the code quality

## Backup Folders

- By default, HQA creates sequential backup folders (e.g., `folder.h2-backup.0`, `folder.h2-backup.1`, etc.).
- Use the `--single-backup` flag to keep only one backup folder (e.g., `folder.h2-backup`).

## Dependencies

HQA depends on:

* [OpenAI python SDK](https://github.com/openai/openai-python) - for sending prompts into any OpenAI compatible server (such as ollama)
* [rich](https://github.com/Textualize/rich) - for rich console output and progressbar

## Author

- **A 1** – [GitHub: aonexyz](https://github.com/aonexyzl)

---

## Buy me a coffee ☕
Love the bot? Wanna fuel more WAGMI vibes? Drop some crypto love to keep the charts lit! 🙌
- **SUI**: `0x6e20d8f6c15aeb42887608eec65b29385f21fa21cfd23302c54fabd813d8cd38`
- **USDT (TRC20)**: `TMoPwVpeC8A2yTc5qotKj8gVXaGTqQwc3L`
- **BNB (BEP20)**: `0x068ff5934e0c30d8763012a6faa0033e7fdcc455`
- **Binance UID**:`899350787`

Every bit helps me grind harder and keep this bot stacking bags! 😎
---

## 🪪 License
MIT © 2025

