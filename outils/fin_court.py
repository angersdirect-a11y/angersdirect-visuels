import sys, json
sys.path.insert(0,'/home/claude/angersdirect-visuels/outils')
import video
orig=video.anim
video.anim=lambda nom,debut,duree,courbe='cubic-bezier(.2,.8,.2,1)': orig(nom,debut*0.55,duree*0.6,courbe)
video.FIN=3.0
sys.argv=['video.py','fin.json','fin_court.mp4']
video.main()
