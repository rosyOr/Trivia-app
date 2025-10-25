from app import create_app
from app.cli import import_opentdb_cmd
from flask import Blueprint, render_template



trivia_bp = Blueprint("trivia", __name__)

app = create_app()
app.register_blueprint(trivia_bp, url_prefix="/trivia")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")








#@app.route("/results")
#def results():
    #return render_template("result.html", score=session["score"])

#@app.route("/ranking")
#def ranking():
    # Basado en la vista vw_ranking_top10
  #  result = db.session.execute("""
   #    SELECT alias, MAX(puntaje_total) AS mejor_puntaje_partida
    #    FROM partida JOIN jugador USING(jugador_id)
     #   GROUP BY alias ORDER BY mejor_puntaje_partida DESC LIMIT 10
    #""").fetchall()
    #return render_template("ranking.html", players=result)



if __name__ == "__main__":
    app.run(debug=True)

app.cli.add_command(import_opentdb_cmd)


