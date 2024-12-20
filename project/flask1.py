from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/function_entry', methods=['GET', 'POST'])
def function_entry():
    if request.method == 'POST':
        function_name = request.form['function_name']
        no_of_return_types = int(request.form['no_of_return_types'])
        no_of_parameters = int(request.form['no_of_parameters'])
        return redirect(url_for('dynamic_fields', 
                                function_name=function_name, 
                                no_of_return_types=no_of_return_types, 
                                no_of_parameters=no_of_parameters))
    return render_template('function_entry.html')

@app.route('/dynamic_fields', methods=['GET', 'POST'])
def dynamic_fields():
    function_name = request.args.get('function_name')
    no_of_return_types = int(request.args.get('no_of_return_types'))
    no_of_parameters = int(request.args.get('no_of_parameters'))

    if request.method == 'POST':
        return_types = []
        parameters = []
        
        # Process return types
        for i in range(no_of_return_types):
            return_type = request.form.get(f'return_type_{i}')
            if return_type in ['list', 'tuple']:
                detail_type = request.form.get(f'return_details_{i}')
                if return_type == 'list':
                    return_types.append(f"List[{detail_type}]")
                else:
                    return_types.append(f"Tuple({detail_type})")
            else:
                return_types.append(return_type)
        
        # Process parameters
        for i in range(no_of_parameters):
            param_type = request.form.get(f'param_{i}')
            if param_type in ['list', 'tuple']:
                detail_type = request.form.get(f'param_details_{i}')
                if param_type == 'list':
                    parameters.append(f"List[{detail_type}]")
                else:
                    parameters.append(f"{param_type}({detail_type})")
            else:
                parameters.append(param_type)

        # Generate the docstring
        docstring = f"{function_name}({', '.join(parameters)}) -> {', '.join(return_types)} :"

        return render_template('final_docstring.html', docstring=docstring)

    return render_template('dynamic_fields.html', 
                           function_name=function_name, 
                           no_of_return_types=no_of_return_types, 
                           no_of_parameters=no_of_parameters)



if __name__ == '__main__':
    app.run(debug=True)
