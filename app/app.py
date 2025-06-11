# This file is the main application file to host the application logic

# Importing gradio and the animate_collatz_sequence function from funcs.py
import gradio as gr
from funcs import animate_collatz_sequence

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            # Adding an application header 
            gr.Markdown("""
            <div style="text-align: center; font-size: 18px;">
                <h1 style="font-size: 32px;">Collatz Branches Animator 🌌</h1>
                <p>Use this interactive tool to generate animations of Collatz branches!</p>
                <h3 style="font-size: 24px;">Instructions:</h3>
                <ol style="display: inline-block; text-align: left; font-size: 18px;">
                    <li><strong>Input the maximum number</strong> for which we compute the Collatz sequence.<code>c</code>.</li>
                    <li><strong>Adjust the maximum number of branches</strong> to animate at once.</li>
                    <li><strong>Adjust the slant angles</strong> to control how the branches move.</li>
                    <li><strong>Choose a colormap</strong> to customize the appearance.</li>
                    <li>Click <strong>"Generate Animation"</strong> to render the video.</li>
                    <li>For more info, see this <a href="https://github.com/ArnelMalubay/collatz-gradio" target="_blank">GitHub repository</a>.</li>
                </ol>
            </div>
            """)
            # Adding all the interactive components of the application
            max_number = gr.Slider(label = 'Specify the maximum number to use for the branches', minimum = 100, maximum = 3000, value = 500, step = 10, interactive = True)
            num_simultaneous = gr.Slider(label = 'Specify the maximum number of branches to animate at once', minimum = 10, maximum = 100, value = 50, step = 10, interactive = True)
            min_slant_angle = gr.Slider(label = 'Specify the minimum slant angle', minimum = 0, maximum = 45, value = 30, step = 5, interactive = True)
            max_slant_angle = gr.Slider(label = 'Specify the maximum slant angle', minimum = 60, maximum = 90, value = 75, step = 5, interactive = True)
            colormap_choices = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2', 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c']
            colormap = gr.Dropdown(label = 'Choose colormap', choices = colormap_choices, value = 'Pastel1', interactive = True)
            submit = gr.Button('Generate Animation', variant = 'huggingface')
            
        video = gr.Video(label = 'Collatz Branches Animation', format = 'mp4', width = 800, height = 1000, interactive = False)

    submit.click(fn = animate_collatz_sequence, inputs = [max_number, num_simultaneous, max_slant_angle, min_slant_angle, colormap], outputs = video)

# To launch the application at any IP address, we need to set server name to 0.0.0.0; server port is Gradio's default port 7860
demo.launch(server_name = "0.0.0.0", server_port = 7860)