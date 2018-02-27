from flask import Flask,flash,session,redirect,url_for, escape,request,render_template,Markup,abort

import os

class Media:

    '''
        Upload files
    '''
    def upload(path):
        if request.method == 'POST':
            f = request.files['the_file']
            supportext = (
                '.png', '.jpg', '.jpeg','.svg',
                'gif','.zip','.html','.css',
                '.js','.wav','.mp3','.mp4','.webm'
            )
            if f.filename.lower().endswith(supportext):
                fileurl = os.path.join(path+'/uploads/',f.filename)
                f.save(fileurl)
                if(os.path.isfile(fileurl)):
                    flash('The file has been uploaded!')
                    return redirect(url_for('media'))
                else:
                    flash('Sorry the file is not uploaded')
                    return redirect(url_for('media'))
            else :
                flash('Sorry only images are support')
                return redirect(url_for('media'))

    '''
        Delete file
    '''
    def delete():
        if request.method == 'POST':
            fileurl = os.path.join(path+'/uploads/',request.form['file'])
            if(os.path.isfile(fileurl)):
                os.remove(fileurl)
                flash('The file has been removed!')
                return redirect(url_for('media'))
            else :
                flash('The file not exists')
                return redirect(url_for('media'))
