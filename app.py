from todaysUnyang import create_app

todaysUnyang = create_app()

todaysUnyang.run(debug = True, host = '0.0.0.0', port = 80)