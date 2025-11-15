import os
from flask import Flask, render_template, request
from db import add_user, update_user, del_user, get_all_users

# base application object
app = Flask(__name__)

# @app.route is a decorator that tells Flask to run the following function when a request for the given path comes in ('/')
@app.route('/')
def home():
    return '<h1>Hestia Home</h1><a href=/userlist>User List</a>'

@app.route('/userlist', methods=['GET', 'POST', 'DELETE'])
def users():
    if request.method == 'GET':
        rows = get_all_users() # list of User objects
        # render_template will render a jinja template, which is basically an HTML file with extra functionality.
        return render_template('userlist.html', users=rows)
    elif request.method == 'POST':
        # request will have all required fields for a user
        if not {'name', 'song_url', 'light_color'} & request.form.keys():
            return None
        name = request.form['name']
        song_url = request.form['song_url']
        light_color = request.form['light_color']

        image = request.files['img']
        filename = f'{name}{os.path.splitext(image.filename)[1]}'
        image.save(os.path.join(app.static_folder, 'uploads', filename))
        img = f'/static/uploads/{filename}'
        add_user(img, name, song_url, light_color)

        rows = get_all_users()
        return render_template('userlist.html', users=rows)
    elif request.method == 'DELETE':
        data = request.get_json()
        user_name = data['user_name']
        del_user(user_name)

        rows = get_all_users()
        return render_template('userlist.html', users=rows)


@app.route('/greet', methods=['GET', 'POST'])
def greet():
    #request is a 'global proxy'. We import it from Flask and it keeps tracks of every request that comes in. Every time a request comes in, Flask pushes a Request object onto the stack. Whenever we call something from request, Flask takes the item at the top of the stack and that is what we are acting on. After the request is handled, the object is popped off the stack to ensure no bleed-over.
    if request.method == 'GET':
        return '''
            <form method="POST">
                <input name="name" placeholder="Your name">
                <button>Go</button>
            </form>
        '''
    else:
           name = request.form['name']
           return f'Hello, {name}'
def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
