#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import *
import json
import logging

from modeles import modeleGSBRV

app = Flask( __name__ )


@app.route( '/visiteurs/<matricule>/<mdp>' , methods = [ 'GET' ] )
def seConnecter( matricule , mdp ) :
	visiteur = modeleGSBRV.seConnecter( matricule , mdp )
	
	if visiteur != None and len( visiteur ) != 0 :
		reponse = make_response( json.dumps( visiteur ) )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'application/json'
		reponse.status_code = 404
	return reponse
		
	
@app.route( '/rapports/<matricule>/<mois>/<annee>' , methods = [ 'GET' ] )
def getRapportsVisite( matricule , mois , annee ) :
	rapports = modeleGSBRV.getRapportsVisite( matricule , mois , annee )

	app.logger.info( "Liste des rapports : " + str(rapports))

	if rapports != None and rapports != [] :
		reponse = make_response( json.dumps( rapports ) )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'application/json'
		reponse.status_code = 404
	return reponse
	

@app.route( '/rapports/echantillons/<matricule>/<numRapport>' , methods = [ 'GET' ] )
def getEchantillonsOfferts( matricule , numRapport ) :
	offres = modeleGSBRV.getEchantillonsOfferts( matricule , numRapport )
	print offres
	
	if offres != None :
		reponse = make_response( json.dumps( offres ) )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'application/json'
		reponse.status_code = 404
	return reponse

	
@app.route( '/praticiens' , methods = [ 'GET' ] )
def getPraticiens() :
	praticiens = modeleGSBRV.getPraticiens()
	
	if praticiens != None :
		reponse = make_response( json.dumps( praticiens ) )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'application/json'
		reponse.status_code = 404
	return reponse
	
@app.route( '/medicaments' , methods = [ 'GET' ] )
def getMedicaments() :
	medicaments = modeleGSBRV.getMedicaments()
	
	if medicaments != None :
		reponse = make_response( json.dumps( medicaments ) )
		reponse.mimetype = 'application/json'
		reponse.status_code = 200
	else :
		reponse = make_response( '' )
		reponse.mimetype = 'application/json'
		reponse.status_code = 404
	return reponse
	
@app.route( '/rapports' , methods = [ 'POST' ] )
def addRapportVisite() :
	unRapport = json.loads( request.data )

	dateVisite = unRapport['visite']
	#app.logger.info("dateVisite : " + dateVisite)

	dateVisite = dateVisite.split("/")
	jour = dateVisite[0]
	mois = dateVisite[1]
	annee = dateVisite[2]

	#app.logger.info("jour : " + jour)
	#app.logger.info("mois : " + mois)
	#app.logger.info("annee : " + annee)

	dateVisite = annee + "-" + mois + "-" + jour

	numRapport = modeleGSBRV.enregistrerRapportVisite( 	unRapport[ 'matricule' ] , 
																unRapport[ 'praticien' ] ,
																dateVisite ,
																unRapport[ 'bilan' ] ,
														  		unRapport[ 'motif' ],
														  		unRapport[ 'coef_confiance' ],
														 		unRapport[ 'date_redaction' ]
  	)
	app.logger.info(
		"Création d'un rapport de visite : "
		+ "\n Matricule : " + json.dumps(unRapport['matricule'])
		+ "\n numPraticien : " + json.dumps(unRapport['praticien'])
		+ "\n Date de visite : " + json.dumps(dateVisite)
		+ "\n Motif : " + json.dumps(unRapport['motif'])
		+ "\n CoefConfiance : " + json.dumps(unRapport['coef_confiance'])
		+ "\n Date de rédaction : " + json.dumps(unRapport['date_redaction'])
	)

	reponse = make_response( '' )
	if numRapport != None :
		objetJSON = {}
		objetJSON['rap_num'] = numRapport
		reponse = make_response(json.dumps(objetJSON))
		reponse.mimetype = 'application/json'
		reponse.headers[ 'Location' ] = '/rapports/%s/%d' % ( unRapport[ 'matricule' ] , numRapport )
		reponse.status_code = 201
		app.logger.info(reponse)
	else :
		reponse.status_code = 409
	return reponse

@app.route( '/rapports/echantillons/<matricule>/<numRapport>' , methods = [ 'POST' ] )
def addEchantillonsOfferts( matricule , numRapport ) :
	echantillons = json.loads( request.data )
	nbEchantillons = modeleGSBRV.enregistrerEchantillonsOfferts( matricule , numRapport , echantillons )
	
	reponse = make_response( '' )												
	if numRapport != None :
		reponse.headers[ 'Location' ] = '/rapports/echantillons/%s/%s' % ( matricule , numRapport )
		reponse.status_code = 201
	else :
		reponse.status_code = 409
	return reponse






if __name__ == '__main__' :
	app.run( debug = True , host = '0.0.0.0' , port = 5000 )


