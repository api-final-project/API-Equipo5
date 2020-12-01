from app import create_app
from flask import Flask, jsonify, request, render_template
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import pymongo
from flask_cors import CORS
import db_config as db

app = create_app()
api = Api(app)
CORS(app)

post_boss_args= reqparse.RequestParser()
post_boss_args.add_argument('id',type=int,help="Error ID is required",required=True)
post_boss_args.add_argument('name',type=str,help="Error Name is required",required=True)
post_boss_args.add_argument('base_hp',type=int,help="Error Base HP is required",required=True)
post_boss_args.add_argument('stage_hp',type=int,help="Error Stage HP is required",required=True)
post_boss_args.add_argument('rooms_appear',type=str,help="Error Room Appear is required",required=True)
post_boss_args.add_argument('image',type=str,help="Error image is required",required=True)
post_boss_args.add_argument('video',type=str,help="Error video is required",required=True)

class Test(Resource):
    def get(self):
        return jsonify({"message":"API working ok"})

class Bosse(Resource):
    def get(self,id):
        self.abort_if_not_exist(id)
        boss = db.db.bosses_binding_of_isaac.find_one({'id':id})
        del boss['_id']
        return jsonify(boss)
    
    def post(self):
        self.abort_if_id_exist(request.json['id'])
        args = post_boss_args.parse_args()
        db.db.bosses_binding_of_isaac.insert_one({
            'id':request.json['id'],
            'name':request.json['name'],
            'base_hp':request.json['base_hp'],
            'stage_hp':request.json['stage_hp'],
            'rooms_appear':request.json['rooms_appear'],
            'image':request.json['image'],
            'video':request.json['video']
        })
        return jsonify({"create":request.json})

    def put(self,id):
        self.abort_if_not_exist(id)
        db.db.bosses_binding_of_isaac.update_one({'id':id},
        {'$set':{
            'id':request.json['id'],
            'name':request.json['name'],
            'base_hp':request.json['base_hp'],
            'stage_hp':request.json['stage_hp'],
            'rooms_appear':request.json['rooms_appear'],
            'image':request.json['image'],
            'video':request.json['video']
        }})
        return jsonify({"update":request.json})
    
    
    def delete(self,id):
        self.abort_if_not_exist(id)
        boss= db.db.bosses_binding_of_isaac.find_one({'id':id})
        del boss['_id']
        db.db.bosses_binding_of_isaac.delete_one({'id':id})
        return jsonify({"delete":boss})

    def abort_if_not_exist(self,id):
        if not db.db.bosses_binding_of_isaac.find_one({'id':id}):
            abort(jsonify({'status':'404', 'error':f'The boss with id:{id} not found'}))
    
    def abort_if_id_exist(self,id):
        if db.db.bosses_binding_of_isaac.find_one({'id':id}):
            abort(jsonify({'status':'409', 'error':f'The boss with id:{id} already exist'}))
            
class AllBosses(Resource):
    def get(self):
        all_bosses = list(db.db.bosses_binding_of_isaac.find())
        for boss in all_bosses:
            del boss['_id']
        return jsonify({'bosses':all_bosses})
    
@app.route('/')
def inicio():
    boss = list(db.db.bosses_binding_of_isaac.find())
    return render_template('index.html', jefes = boss)

@app.route("/boss/<int:id>")
def boss(id):
    boss = dict(db.db.bosses_binding_of_isaac.find_one({"id":id}))
    return render_template('Boss.html', jefe = boss)             

api.add_resource(Test,'/test/')
api.add_resource(AllBosses,'/all_bosses/')
api.add_resource(Bosse,'/new/boss/','/boss/<int:id>')

if __name__ == "__main__":
    app.run(load_dotenv=True,port=8080)

