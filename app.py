from flask import Flask, jsonify, request, Response
from pymongo import MongoClient
from bson.json_util import dumps
import json
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb+srv://a01177640:Oc0AMR2QKYeXgFOq@mty365.154j6qb.mongodb.net/?retryWrites=true&w=majority', 
                        tls=True,
                        tlsAllowInvalidCertificates=True)
db = client.Mty365
collection = db.spots


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/form')
def form():
	return render_template('form.html')



#git 
@app.route('/add_spot', methods=['POST'])
def add_spot():
    spotInfo = request.get_json()  # Assumes the request contains a JSON payload with the new document data
    new_spot = {
        'title': spotInfo['title'],
        'author': spotInfo['author'],
        'location': spotInfo['location'],
        'category': spotInfo['category'],
        'image': spotInfo['image'],
        'description': spotInfo['description'],
    }
    result = collection.insert_one(new_spot)
    return f"Inserted document with ID {result.inserted_id}"

@app.route('/spots')
def get_spots():
    spotsList = collection.find()
    spots = []
    for spot in spotsList:
        spots.append(json.loads(json.dumps(spot, default=str)))
    return jsonify(spots)

@app.route('/update_spot/<id>', methods= ['PATCH'])
def update_spot(id):
    
    title = request.form['title']
    author = request.form['author']
    location = request.form['location']
    category = request.form['category']
    image= request.form['image']
    description= request.form['description']
    try: 
        dbResponse = collection.update_one(
			{"_id": ObjectId(id)},
			{"$set": {'title': title, 
             'author': author,
             'location': location,
             'category': category,
             'image': image,
             'description': description
             }}
		)
        
        if dbResponse.modified_count == 1:
            return Response(
			response= json.dumps(
				{"message": "object updated"}),
				status= 200,
				mimetype= "application/json"
			)
            
    except Exception as ex:
        print("****")
        print(ex)
        print("****")
        
        return Response(
			response= json.dumps(
				{"message": "unable to update object"}),
			status=500,
			mimetype="application/json"
			)

@app.route("/delete_spot/<id>", methods = ["DELETE"])
def delete_spot(id):
    
    try: 
        dbResponse = collection.delete_one({"_id": ObjectId(id)})
        return Response(
			response= json.dumps(
				{"message": "user deleted", "id": f"{id}"}),
				status= 200,
				mimetype= "application/json"
			)
        
    except Exception as ex:
        print("****")
        print(ex)
        print("****")
        
        return Response(
			response= json.dumps(
				{"message": "unable to delete object"}),
			status=500,
			mimetype="application/json"
			)
        
if __name__ == '__main__':
    app.run()



'''


client = pymongo.MongoClient("mongodb+srv://<username>:<password>@mty365.154j6qb.mongodb.net/?retryWrites=true&w=majority")
db = client['MTY365db']
spots = db.spots

@app.route("/list")
def lists ():
	#Display the all Tasks
	todos_l = todos.find()
	a1="active"
	return render_template('index.html',a1=a1,todos=todos_l,t=title,h=heading)

@app.route("/action", methods=['POST'])
def action ():
	#Adding a Task
	name=request.values.get("name")
	desc=request.values.get("desc")
	date=request.values.get("date")
	pr=request.values.get("pr")
	todos.insert({ "name":name, "desc":desc, "date":date, "pr":pr, "done":"no"})
	return redirect("/list")

@app.route("/remove")
def remove ():
	#Deleting a Task with various references
	key=request.values.get("_id")
	todos.remove({"_id":ObjectId(key)})
	return redirect("/")

@app.route("/update")
def update ():
	id=request.values.get("_id")
	task=todos.find({"_id":ObjectId(id)})
	return render_template('update.html',tasks=task,h=heading,t=title)


@app.route("/search", methods=['GET'])
def search():
	#Searching a Task with various references

	key=request.values.get("key")
	refer=request.values.get("refer")
	if(key=="_id"):
		todos_l = todos.find({refer:ObjectId(key)})
	else:
		todos_l = todos.find({refer:key})
	return render_template('searchlist.html',todos=todos_l,t=title,h=heading)

'''
