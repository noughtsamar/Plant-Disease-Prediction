from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import keras
import numpy as np
from PIL import Image
import tensorflow as tf

app = Flask(__name__)
model1 = keras.models.load_model('potato.h5')
model2 = keras.models.load_model('maize_corn.h5')
model3 = keras.models.load_model('rice.h5')
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/',methods=['POST'])
def upload_image():
    leaf = request.values['leaf']
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = Image.open('./static/uploads/'+filename)
    image = np.asarray(img)
    a= tf.convert_to_tensor(image)
    image=a.numpy().astype("uint8")
    image.resize(1, 256, 256, 3)
    b=np.array(image)
    potato_class=['Early Blight','Healthy','Late Blight']
    maize_class=['Blight','Common-Rust','Gray_Leaf_Spot','Healthy']
    rice_class = ['Bacterial Leaf Blight','Brown Spot','Leaf Smut']
    links=['healthy', 'healthy', 'healthy']
    if (leaf == 'potato'):
        prediction = potato_class[np.argmax(model1.predict(b)[0])]
        if (prediction == "Early Blight"):
            links = ['https://www2.ipm.ucanr.edu/agriculture/potato/Early-Blight/#:~:text=Early%20blight%20can%20be%20minimized,enough%20to%20cause%20economic%20loss','https://www.gardeningknowhow.com/edible/vegetables/potato/potato-early-blight-treatment.htm','https://www.gardeningknowhow.com/edible/vegetables/potato/potato-early-blight-treatment.htm']
        if (prediction == "Late Blight"):
            links = ['https://www2.ipm.ucanr.edu/agriculture/potato/late-blight/#:~:text=Late%20blight%20is%20controlled%20by,foliage%20each%20day%20is%20important','https://www.planetnatural.com/pest-problem-solver/plant-disease/late-blight/','https://www.planetnatural.com/pest-problem-solver/plant-disease/late-blight/']
        #prediction = model1.predict(b)
    elif (leaf == 'maize'):
        prediction = maize_class[np.argmax(model2.predict(b)[0])]
        if (prediction == 'Blight'):
            links= ['https://plantix.net/en/library/plant-diseases/100161/southern-leaf-blight-of-maize/','https://www.lfl.bayern.de/ips/blattfruechte/050760/index.php','https://apps.lucidcentral.org/pppw_v10/text/web_full/entities/maize_northern_leaf_blight_226.htm']
        #prediction = model2.predict(b)
        if (prediction == 'Common-Rust'):
            links = ['https://www.pioneer.com/us/agronomy/common_rust_corn_cropfocus.html#:~:text=Common%20rust%20is%20a%20foliar,yield%20loss%20than%20southern%20rust','https://extension.umn.edu/corn-pest-management/common-rust-corn','https://ohioline.osu.edu/factsheet/plpath-cer-02']
        if (prediction=='Gray_Leaf_Spot'):
            links = ['https://extension.umn.edu/corn-pest-management/gray-leaf-spot-corn#:~:text=Gray%20leaf%20spot%20is%20typically,high%20humidity%20and%20warm%20conditions','https://en.wikipedia.org/wiki/Corn_grey_leaf_spot','https://www.pioneer.com/us/agronomy/gray_leaf_spot_cropfocus.html']
    elif (leaf == 'rice'):
        prediction = rice_class[np.argmax(model3.predict(b)[0])]
        if (prediction == 'Bacterial Leaf Blight'):
            links = ['https://www.plantwise.org/KnowledgeBank/pmdg/20167800391','https://www.plantwise.org/KnowledgeBank/pmdg/20167800391','https://www.plantwise.org/KnowledgeBank/pmdg/20167800391']
        if (prediction == 'Brown Spot'):
            links = ['http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/brown-spot#:~:text=Use%20fungicides%20(e.g.%2C%20iprodione%2C,infection%20at%20the%20seedling%20stage.','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/narrow-brown-spot','http://www.knowledgebank.irri.org/training/fact-sheets/pest-management/diseases/item/narrow-brown-spot','https://www.gardeningknowhow.com/edible/grains/rice/treating-rice-brown-leaf-spot.htm']
        if (prediction == 'Leaf Smut'):
            links = ['https://www.sprinklersystemsburlington.com/lawn-diseases-leaf-smut.html','https://www.gardeningknowhow.com/edible/grains/rice/how-to-treat-leaf-smut-of-rice.htm','https://www.gardeningknowhow.com/edible/grains/rice/how-to-treat-leaf-smut-of-rice.htm']
    else:
        prediction = maize_class[np.argmax(model2.predict(b)[0])]
        #prediction = model2.predict(b)
    #prediction = model1.predict(b)
    return render_template('index.html', filename=prediction,link1 = links[0],link2 = links[1],link3=links[2])
if __name__ == "__main__":
    app.run(debug=True)