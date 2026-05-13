from app import create_app

app = create_app()

if __name__ == '__main__':
    # O debug=True faz o servidor reiniciar sozinho quando você salva um arquivo
    app.run(debug=True)