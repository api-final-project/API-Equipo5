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
