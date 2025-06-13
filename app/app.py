# This file is the main application file to host the application logic

# Importing gradio and the plot_collatz_sequence function from funcs.py
import gradio as gr
from funcs import plot_collatz_sequence

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            # Adding an application header 
            gr.Markdown("""
            <div style="text-align: center; font-size: 18px;">
                <h1 style="font-size: 32px;">Collatz Branches Visualizer 🌲</h1>
                <p>Use this interactive tool to generate visualizations of Collatz branches!</p>
                <h3 style="font-size: 24px;">Instructions:</h3>
                <ol style="display: inline-block; text-align: left; font-size: 18px;">
                    <li><strong>Input the maximum number</strong> for which we compute the Collatz sequence.</li>
                    <li><strong>Adjust the slant angle</strong> to control how the branches move.</li>
                    <li><strong>Adjust the fan angle</strong> to control how "spread out" the graphic is.</li>
                    <li><strong>Choose a colormap</strong> to customize the appearance.</li>
                    <li><strong>Adjust the color period</strong> parameter to specify how many times each unique color will be repeated.</li>
                    <li>Click <strong>"Generate Visual"</strong> to render the graphic.</li>
                    <li>For more info, see this <a href="https://github.com/ArnelMalubay/collatz-gradio" target="_blank">GitHub repository</a>.</li>
                </ol>
            </div>
            """)
            # Adding all the interactive components of the application
            max_number = gr.Slider(label = 'Specify the maximum number to use for the branches', minimum = 1000, maximum = 20000, value = 2000, step = 10, interactive = True)
            slant_angle = gr.Slider(label = 'Specify the slant angle', minimum = 45, maximum = 90, value = 90, step = 5, interactive = True)
            fan_angle = gr.Slider(label = 'Specify the fan angle', minimum = 45, maximum = 90, value = 90, step = 5, interactive = True)
            colormap_choices = ['Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'Pastel1', 'Pastel2', 'inferno', 'binary', 'magma', 'cividis', 'viridis', 'plasma', 'Paired', 'Accent', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'rainbow', 'jet', 'turbo', 'gray', 'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool', 'hot', 'copper', 'Dark2']
            colormap = gr.Dropdown(label = 'Choose colormap', choices = colormap_choices, value = 'Set1', interactive = True)
            colorperiod = gr.Slider(label = 'Specify the color period', minimum = 1, maximum = 20, value = 5, step = 1, interactive = True) 
            # Adding a button to generate the visual
            submit = gr.Button('Generate Visual', variant = 'huggingface')
            
        image = gr.Image(label = 'Collatz Branches Graphic', format = 'png', width = 800, height = 1000, interactive = False)

    submit.click(fn = plot_collatz_sequence, inputs = [max_number, slant_angle, fan_angle, colormap, colorperiod], outputs = image)

# To launch the application at any IP address, we need to set server name to 0.0.0.0; server port is Gradio's default port 7860
demo.launch(server_name = "0.0.0.0", server_port = 7860)