# ChessQL
To expand my knowledge of GraphQL I wanted to implement a small API.

This is an API which could be used in combination with ChessApp: https://github.com/Allertj/ChessApp, which was used as a template for its basic database functions. 

### Architecture
This API uses PostGreSQL and SQLAlchemy for its database functions, Flask for its exposing of the "/graphql" route, Flask-JWT-Extended for its security and Graphene for the implementation of GraphQL. A full list of all python dependencies is available in the requirements.txt file. The GraphQL schema is on the bottom of this README. 

### Build instructions
First, place secure, long strings in both the JWT_SECRET_KEY and DB_SECRET_KEY fields in .env file as the project will not run without them. Also add strings to the DBUSERNAME, DBPASSWORD and DBDATABASE fields. 

There are two basic setups: simple development as a default and a full production with Docker containers. For simple development, launch docker compose to activate the database:
```docker-compose up --build``` and launch the main python file from the root of the project: ```python main.py``` or ```python3.9 main.py``` The API should be online on: ```http://localhost:4000/graphql``` This 4000 default port can be changed in .env file. 

To use full production setup, uncomment the second container in the docker-compose.yml file, and the production values in the bottom of the .env file. Comment out the development values block above that. Use ```docker-compose up --build``` to launch everything. The API should be online on ```http://localhost:1337/graphql``` The default port can be changed in the 
.env file. 

### Security
Use the **signup** and **login** mutations to get an access token. All other graphql queries and mutations require one in its header. The header should look like this: ```{"x-access-token: token}``` This markup can be changed in the main.py file. Some of the queries and mutations also require admin access, these methods are decorated with the @admin_required decorator. The admin-access is embedded in the access token. To elevate a user to admin, use the "promote_user_to_admin(userid)" function in database/db_user_mutations.            

### Workflows and Unittests
I have written a few unittests for some of the routes. Most involve creating a dummy user, login it in and performing some actions. Coverage is by no means meant to be complete. All traces should be removed from the database after completion. The unittests are also part of a Github Workflow, which is triggered after each commit. All unittests are run and the results can be viewed in the actions tab. 

### Schema
This is the current schema:

```
scalar DateTime

type Games implements Node {
  gameid: ID!
  player0id: Int
  player1id: Int
  status: String
  result: String
  timeStarted: DateTime
  lastChange: DateTime
  turn: Int
  unverifiedMove: String
  drawProposed: String
  gameasjson: String
  id: ID!
}

type Login {
  user: User
  accessToken: String
}

type MyMutations {
  signup(email: String, password: String, username: String): Signup
  login(email: String, password: String): Login
  sendMove(gameid: Int, move: String, userid: Int): SendMove
  startGame(userid: Int): StartGame
}

interface Node {
  id: ID!
}

type Query {
  allUsers: [User]
  allGames: [Games]
  admins: [User]
  game(gameid: Int): Games
  user(userid: Int): User
}

type SendMove {
  result: String
}

type Signup {
  user: User
}

type StartGame {
  result: String
  newGame: Games
}

type User implements Node {
  userid: ID!
  username: String
  email: String
  password: String
  wins: Int!
  draws: Int!
  loses: Int!
  openGames: Int!
  id: ID!
  games: [Games]
}
```