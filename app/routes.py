import base64

from app import app
from flask import render_template, request

stypelist = ['Base64', 'Base85', 'Ascii85', 'z85']
functionslist = ['B64e', 'B64d']

# load main landing page
@app.route('/', methods=['GET', 'POST'])
def index():
    
    # catch POST request to process the form data [e_box]
    if request.method == 'POST':
        
        # check if submit form data is empty; HTML form required attribute enforced.
        if request.form['e_box'] == '':
            
            mymsg = 'Please enter a value'
            
            return render_template('ireturndata.html', output_data=mymsg)
        
        else:
            try:
                
                # check whether encode or decode and which encode functions
                if request.form['stype'] == 'B64e' and request.form['functions'] == 'Base64':

                    file = request.form['e_box']

                    encoded_data = base64.b64encode(file.encode('ascii'))
                    
                    f_decoded_data = encoded_data.decode('ascii')
                    
                    return render_template('returndata.html', output_data=f_decoded_data)
                
                if request.form['stype'] == 'B64d' and request.form['functions'] == 'Base64':
                    file = request.form['e_box']

                    # catch exception
                    try:
                        
                        '''
                        check data length, then get reminder of modulo operation devide by 4
                        follow with multiply with passing string "="
                        ensure that the resulting string is correctly padded with the necessary number of "="
                        characters to make its length a multiple of 4.
                        '''
                        decoded_data = base64.b64decode(file + "=" * (-len(file) % 4))
                        
                        f_decoded_data = decoded_data.decode("ascii")
                    
                        
                    except Exception as e:
                        mymsg = 'Please enter a valid Base64 string'
                        return render_template('ireturndata.html', output_data=mymsg)
                    
                    return render_template('returndata.html', output_data=f_decoded_data)
                
                if request.form['stype'] == 'B64e' and request.form['functions'] == 'Base85':
                    file = request.form['e_box']

                    encoded_data = base64.b85encode(file.encode('ascii'))
                    
                    f_decoded_data = encoded_data.decode("ascii")
                    
                    return render_template('returndata.html', output_data=f_decoded_data)
                
                if request.form['stype'] == 'B64d' and request.form['functions'] == 'Base85':
                    file = request.form['e_box']

                    try:
                        decoded_data = base64.b85decode(file)
                        
                        f_decoded_data = decoded_data.decode("ascii")

                    except Exception as e:
                        mymsg = 'Please enter a valid Base85 string'
                        return render_template('ireturndata.html', output_data=mymsg)
                    
                    return render_template('returndata.html', output_data=f_decoded_data)
                
                if request.form['stype'] == 'B64e' and request.form['functions'] == 'Ascii85':
                    file = request.form['e_box']

                    encoded_data = base64.a85encode(file.encode('ascii'))
                    
                    f_decoded_data = encoded_data.decode("ascii")
                    
                    return render_template('returndata.html', output_data=f_decoded_data)
                
                if request.form['stype'] == 'B64d' and request.form['functions'] == 'Ascii85':
                    file = request.form['e_box']
                    
                    try:
                        decoded_data = base64.a85decode(file)
                    
                        f_decoded_data = decoded_data.decode("ascii")
                    except Exception as e:
                        mymsg = 'Please enter a valid Base85 string'
                        return render_template('ireturndata.html', output_data=mymsg)

                    
                    return render_template('returndata.html', output_data=f_decoded_data)
                
                if request.form['stype'] == 'B64e' and request.form['functions'] == 'z85':
                    file = request.form['e_box']

                    encoded_data = base64.z85encode(file.encode('ascii'))
                    
                    f_decoded_data = encoded_data.decode("ascii")
                    
                    return render_template('returndata.html', output_data=f_decoded_data)
                
                if request.form['stype'] == 'B64d' and request.form['functions'] == 'z85':
                    file = request.form['e_box']

                  
                    try:
                        decoded_data = base64.z85decode(file)
                    
                        f_decoded_data = decoded_data.decode("ascii")
                    except Exception as e:
                        mymsg = 'Please enter a valid Base85 string'
                        return render_template('ireturndata.html', output_data=mymsg)
                    
                    return render_template('returndata.html', output_data=f_decoded_data)
                
                else:
                    if request.form['stype'] not in functionslist or request.form['functions'] not in stypelist:
                        mymsg = 'Please select a valid function and style'
                        return render_template('ireturndata.html', output_data=mymsg)
            
            # exception occurs return error message
            except Exception as e:
                mymsg = 'something went wrong, please try again'
                return render_template('ireturndata.html', output_data=mymsg)
        
    # catch GET request    
    if request.method == 'GET':
        
        return render_template('index.html', title='encode and decode')

    # catch anything else beside POST and GET request
    else:
        return render_template('index.html', title='encode and decode')


# handle 404 respond
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# handle 500 respond
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500