"""
app.py
------
Language Translator Application
A modern, web-based multi-language text translation system using Gradio & deep-translator.
Designed for 3rd-year B.Tech internship demonstration and classroom presentation.
"""

import sys

# Ensure standard output supports UTF-8 on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import gradio as gr
from translator import get_available_languages, translate_text

# Fetch dynamic supported languages list
supported_languages = get_available_languages()

# Source options include 'Auto Detect' as the first option
source_language_options = ["Auto Detect"] + supported_languages
target_language_options = supported_languages

# Custom CSS for Light Glassmorphism SaaS Aesthetic
CUSTOM_CSS = """
/* Import modern typography */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

body, .gradio-container {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background: linear-gradient(135deg, #f4f7fc 0%, #eef2ff 50%, #f8fafc 100%) !important;
    min-height: 100vh;
}

/* Glassmorphism Card Style */
.glass-panel {
    background: rgba(255, 255, 255, 0.78) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border: 1px solid rgba(255, 255, 255, 0.85) !important;
    border-radius: 18px !important;
    padding: 22px !important;
    box-shadow: 0 10px 30px rgba(30, 41, 59, 0.05) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-panel:hover {
    box-shadow: 0 16px 36px rgba(37, 99, 235, 0.08) !important;
    border-color: rgba(191, 219, 254, 0.8) !important;
}

/* Header Styling */
.header-box {
    text-align: center;
    padding: 26px 20px 20px 20px;
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.85);
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(37, 99, 235, 0.05);
    margin-bottom: 22px;
}

.main-title {
    font-size: 2.1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #4f46e5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}

.subtitle {
    font-size: 1.05rem;
    color: #475569;
    font-weight: 400;
    margin: 0;
}

/* Primary Translate Button with Subtle Glow */
.translate-btn {
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.32) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}

.translate-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.45) !important;
    filter: brightness(1.04) !important;
}

.translate-btn:active {
    transform: translateY(0px) !important;
}

/* Secondary Utility Buttons */
.action-btn {
    background: rgba(255, 255, 255, 0.85) !important;
    color: #334155 !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.action-btn:hover {
    background: #f8fafc !important;
    border-color: #94a3b8 !important;
    transform: translateY(-1px) !important;
}

/* Form element enhancements */
textarea {
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
    background: rgba(255, 255, 255, 0.9) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
}

/* Architecture info badge */
.tech-badge {
    text-align: center;
    font-size: 0.83rem;
    color: #64748b;
    margin-top: 24px;
    padding: 12px 18px;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 12px;
    border: 1px dashed rgba(203, 213, 225, 0.9);
}
"""


def on_translate_click(input_text, source_lang, target_lang):
    """
    Event handler triggered when the user clicks '✨ Translate'.
    Calls the backend translator module and returns the result.
    """
    return translate_text(input_text, source_lang, target_lang)


def on_clear_click():
    """
    Clears both the input and translated textboxes.
    """
    return "", ""


def on_swap_languages(source_lang, target_lang):
    """
    Swaps source and target languages.
    If source is 'Auto Detect', swaps target into source and defaults target to 'English'.
    """
    if source_lang == "Auto Detect":
        new_source = target_lang
        new_target = "English" if target_lang != "English" else "Hindi"
    else:
        new_source = target_lang
        new_target = source_lang
    return new_source, new_target


def on_copy_click(text):
    """
    Notifies the user when text has been copied.
    Actual clipboard copy happens via client-side JavaScript.
    """
    if text and text.strip():
        gr.Info("Translation copied to clipboard!")
    else:
        gr.Warning("No text available to copy.")


# Build the Gradio Blocks Interface
with gr.Blocks(title="Language Translator Application") as demo:

    # Embed Glassmorphism Styling
    gr.HTML(f"<style>{CUSTOM_CSS}</style>")

    # Header Card
    gr.HTML(
        """
        <div class="header-box">
            <h1 class="main-title">🌐 Language Translator</h1>
            <p class="subtitle">Translate text quickly and easily between multiple languages.</p>
        </div>
        """
    )

    with gr.Row(equal_height=True):
        # Left Panel: Input Section
        with gr.Column(scale=1, elem_classes=["glass-panel"]):
            gr.Markdown("### 📝 Input Section")

            source_dropdown = gr.Dropdown(
                label="From Language",
                choices=source_language_options,
                value="Auto Detect",
                interactive=True,
                info="Select input language or let the system detect automatically"
            )

            input_textbox = gr.Textbox(
                label="Text to be translated",
                placeholder="Enter the text you want to translate...",
                lines=7,
                max_lines=12,
                buttons=["copy"]
            )

        # Right Panel: Output Section
        with gr.Column(scale=1, elem_classes=["glass-panel"]):
            gr.Markdown("### 🎯 Output Section")

            target_dropdown = gr.Dropdown(
                label="To Language",
                choices=target_language_options,
                value="Hindi" if "Hindi" in target_language_options else target_language_options[0],
                interactive=True,
                info="Select the language you want to translate into"
            )

            output_textbox = gr.Textbox(
                label="Translated Text",
                placeholder="The translated result will appear here...",
                lines=7,
                max_lines=12,
                interactive=False,
                buttons=["copy"]
            )

    # Action Buttons Bar
    with gr.Row():
        translate_button = gr.Button(
            "✨ Translate",
            variant="primary",
            scale=3,
            elem_classes=["translate-btn"]
        )

        swap_button = gr.Button(
            "⇄ Swap Languages",
            variant="secondary",
            scale=1,
            elem_classes=["action-btn"]
        )

        copy_button = gr.Button(
            "📋 Copy Translation",
            variant="secondary",
            scale=1,
            elem_classes=["action-btn"]
        )

        clear_button = gr.Button(
            "Clear",
            variant="secondary",
            scale=1,
            elem_classes=["action-btn"]
        )

    # Interactive Event Bindings
    # 1. Translate Button Click
    translate_button.click(
        fn=on_translate_click,
        inputs=[input_textbox, source_dropdown, target_dropdown],
        outputs=[output_textbox]
    )

    # 2. Swap Languages Button Click
    swap_button.click(
        fn=on_swap_languages,
        inputs=[source_dropdown, target_dropdown],
        outputs=[source_dropdown, target_dropdown]
    )

    # 3. Clear Button Click
    clear_button.click(
        fn=on_clear_click,
        inputs=[],
        outputs=[input_textbox, output_textbox]
    )

    # 4. Copy Translation Button Click (Client-side Clipboard JS + Toast)
    copy_button.click(
        fn=on_copy_click,
        inputs=[output_textbox],
        outputs=[],
        js="(text) => { if (text && text.trim()) { navigator.clipboard.writeText(text); } }"
    )

    # Architecture & Technology Summary (for viva and presentation)
    gr.HTML(
        """
        <div class="tech-badge">
            <strong>Architecture Flow:</strong> User Input ➔ Gradio UI ➔ Translation Logic (translator.py) ➔ Deep Translator (GoogleTranslator) ➔ Google Translate Service ➔ Gradio Output
            <br>
            <span style="font-size: 0.78rem; color: #94a3b8;">
                Built with Python & Gradio • Real-time External Translation Service Integration • 130+ Supported Languages
            </span>
        </div>
        """
    )


# Application Entry Point
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print(">> Starting Language Translator Application...")
    print(">> Local UI will launch at: http://127.0.0.1:7860")
    print("=" * 60 + "\n")

    # Launch local server
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        theme=gr.themes.Soft(primary_hue="blue", neutral_hue="slate"),
        css=CUSTOM_CSS,
        share=False
    )
