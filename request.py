import requests
import urllib
import zipfile
import os
import shutil
from pathlib import Path
from yattag import Doc
from yattag import indent
from jinja2 import Template
from flask import Flask, render_template
from natsort import natsorted
import dateutil.parser

#request function
def request(github_username, github_repoName):
    gitHubAPI_URL_getTags = f"https://api.github.com/repos/{github_username}/{github_repoName}/releases"
    response = requests.get(gitHubAPI_URL_getTags, auth=(github_username, github_repoName)) 
    data = response.json()
    return data

#request checkerframework release
github_username = "eisop"
github_repoName = "checker-framework"
data = request(github_username,github_repoName)

#request  annotation-tools release
annotation_repoName = "annotation-tools"
annotation_gitHubAPI_URL_getTags = f"https://api.github.com/repos/{github_username}/{annotation_repoName}/releases"
data_annotation_tools = request(github_username,annotation_repoName)


if not os.path.exists('./cf'):
    os.makedirs('./cf')

root,dirs,files = next(os.walk('./cf', topdown=True)) #list directories and files in ./cf directory

def get_release_info(data,folder):
    for i in range(len(data)):
        file_path = folder+"/"+data[i]['tag_name']+".zip"
        file = data[i]['tag_name']+".zip"
        if file not in files:
            print("Downloading "+file)
            urllib.request.urlretrieve(data[i]['assets'][0]['browser_download_url'], file_path)
            print("Downloaded "+file)
            zip_file_path = "./"+folder+ "/"+file
            if(folder =="cf"): #this is because the way the zip file is created. If the zipfile change,this will need to be changed
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall("./"+folder)
            else:
                with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                    zip_ref.extractall("./afu/"+data[i]['tag_name'])
        if(folder =="afu"):
            #create symlink for .zip
            if not os.path.islink('./afu/'+data[i]['tag_name']+"/annotation-file-utilities/annotation-tools-"+data[i]['tag_name']+".zip"):
                os.symlink(os.path.abspath("./afu/"+data[i]['tag_name']+".zip"), os.path.abspath("./afu/"+data[i]['tag_name']+"/annotation-file-utilities/annotation-tools-"+data[i]['tag_name']+".zip"))
            #change annotation-tools-utilities.html to index.html
            if not os.path.islink(os.path.abspath("./afu/"+data[i]['tag_name']+"/annotation-file-utilities/index.html")):
                os.symlink(os.path.abspath("./afu/"+data[i]['tag_name']+"/annotation-file-utilities/annotation-file-utilities.html"), os.path.abspath("./afu/"+data[i]['tag_name']+"/annotation-file-utilities/index.html"))
            #create a symlink for annotation-file-utilities
            if not os.path.islink(os.path.abspath("./cf/checker-framework-"+data[i]['tag_name']+"/annotation-file-utilities")):
                # print("not exists"+data_annotation_tools[i]['tag_name']+"\n")
                os.symlink(os.path.abspath("./afu/"+data[i]['tag_name']+"/annotation-file-utilities"), os.path.abspath("./cf/checker-framework-"+data[i]['tag_name']+"/annotation-file-utilities"))
    
    return 


#download checkerframework releases


get_release_info(data,"cf")


root,dirs,files = next(os.walk('./cf', topdown=True)) 
# print(dirs)
latest_release = natsorted(dirs)[-1] #last element after sort is newest release

# extract Javadoc HTML files to cf/checker-framework-$release/api
for i in natsorted(dirs):
    dir_path = i
    file_path = "./cf/"+dir_path+"/checker/dist/checker-javadoc.jar"
    # print(file_path)
    my_file = Path(file_path)
    if my_file.is_file():
        print(file_path,"found")
        if not Path("./cf/"+dir_path+"/api").is_dir():
            print("folder not exits, createing... ","./cf/"+dir_path+"/api")
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall("./cf/"+dir_path+"/api")
    else:
        print(file_path, "not found")
    
    #download index.html
    homepage = requests.get("https://raw.githubusercontent.com/eisop/checker-framework/"+dir_path+"/docs/checker-framework-webpage.html")
    homepage_text = homepage.text
    with open("./cf/"+dir_path+"/index.html", "w") as f:
        f.write(homepage_text)

    #rename manual.html to index.html
    if not os.path.islink(os.path.abspath("./cf/"+dir_path+"/docs/manual/index.html")):
        os.symlink(os.path.abspath("./cf/"+dir_path+"/docs/manual/manual.html"), os.path.abspath("./cf/"+dir_path+"/docs/manual/index.html"))
    
    #rename manual.pdf to checker-framework-manual.pdf
    if not os.path.islink(os.path.abspath("./cf/"+dir_path+"/docs/manual/checker-framework-manual.pdf")):
        os.symlink(os.path.abspath("./cf/"+dir_path+"/docs/manual/manual.pdf"), os.path.abspath("./cf/"+dir_path+"/docs/manual/checker-framework-manual.pdf"))

    #create symlink for .zip, Docs/manual, Docs/tutorial, Docs/changelog, afu/annotation-tools-utilities
    if not os.path.islink(os.path.abspath("./cf/"+dir_path+"/"+dir_path+".zip")):
        os.symlink(os.path.abspath("./cf/"+dir_path+".zip"), os.path.abspath("./cf/"+dir_path+"/"+dir_path+".zip"))

    if not os.path.islink(os.path.abspath("./cf/"+dir_path+"/manual")):
        os.symlink(os.path.abspath("./cf/"+dir_path+"/Docs/manual"), os.path.abspath("./cf/"+dir_path+"/manual"))

    if not os.path.islink(os.path.abspath("./cf/"+dir_path+"/tutorial")):
        os.symlink(os.path.abspath("./cf/"+dir_path+"/Docs/tutorial"), os.path.abspath("./cf/"+dir_path+"/tutorial"))
    
    if not os.path.islink(os.path.abspath("./cf/"+dir_path+"/CHANGELOG.md")):
        os.symlink(os.path.abspath("./cf/"+dir_path+"/Docs/CHANGELOG.md"), os.path.abspath("./cf/"+dir_path+"/CHANGELOG.md"))
    
if not os.path.exists('./afu'):
    os.makedirs('./afu')

root,dirs,files = next(os.walk('./afu', topdown=True)) #list directories and files in ./cf directory
#download annotation-tool releases
get_release_info(data_annotation_tools,"afu")
