import os
from flask import Flask, render_template, request
from db import add_user, update_user, del_user, get_all_users
from actions import actions_pretty

# base application object
app = Flask(__name__)

# @app.route is a decorator that tells Flask to run the following function when a request for the given path comes in ('/')
@app.route('/')
def home():
    return '<h1>Hestia Home</h1><a href=/userlist>User List</a>'


@app.route('/actions')
def actions():
    return render_template('actions.html', actions_list=actions_pretty('actions.json'))

@app.route('/userlist', methods=['GET', 'POST', 'DELETE'])
def users():
    if request.method == 'GET':
        rows = get_all_users() # list of User objects
        # render_template will render a jinja template, which is basically an HTML file with extra functionality.
        return render_template('userlist.html', users=rows)
    elif request.method == 'POST':
        match request.form['type']:
            case 'create_user':
                name = request.form['name']
                song_url = request.form['song_url']
                light_color = request.form['light_color']

                image = request.files['img']
                filename = f'{name}{os.path.splitext(image.filename)[1]}'
                image.save(os.path.join(app.static_folder, 'uploads', filename))
                img = f'/static/uploads/{filename}'
                add_user(img, name, song_url, light_color)
            case 'update_picture':
                pass
            case 'update_name':
                try:
                    # request.form will have 'new_name', 'original_name' and 'type'
                    new_name = request.form['new_name']
                    if new_name == '':
                        raise ValueError('new_name is empty')
                    original_name = request.form['original_name']
                    update_user(original_name, name=new_name)
                except ValueError as e:
                    print(e)
            case 'update_song_url':
                try:
                    #request.form will have 'new_song_url', 'user_name' and 'type'
                    new_song_url = request.form['new_song_url']
                    if new_song_url == '':
                        raise ValueError('new_song_url is empty.')
                    user_name = request.form['user_name']
                    update_user(user_name, song_url=new_song_url)
                except ValueError as e:
                    print(e)
            case 'update_light_color':
                try:
                    #request.form will have 'new_light_color', 'user_name', and 'type'.
                    new_light_color = request.form['new_light_color']
                    if new_light_color == '':
                        raise ValueError('new_light_color is empty.')
                    user_name = request.form['user_name']
                    update_user(user_name, light_color=new_light_color)
                except ValueError as e:
                    print(e)
            case _:
                raise ValueError('No Type field provided in POST /userlist.')

        rows = get_all_users()
        return render_template('userlist.html', users=rows)
    elif request.method == 'DELETE':
        data = request.get_json()
        user_name = data['user_name']
        del_user(user_name)

        rows = get_all_users()
        return render_template('userlist.html', users=rows)

def main():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    main()
