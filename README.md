###ChessQL
This is a demo GraphQL API written in Python with Flask, Graphene, SQLAlchemy and PostgreSQL. 

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
<!-- This GraphQLServer is written in Kotlin. It has a PostgreSQL database combined with a Redis cache. It uses "graphql-kotlin-spring-server" a handy library which turns Kotlin functions straight into GraphQL queries, mutations and subscriptions.

Further info: https://opensource.expediagroup.com/graphql-kotlin/docs/server/spring-server/spring-overview/

When starting the server the current schema is printed. Use registerUser and loginUser mutations and queries to get a JsonWebToken, which needs to be added to Authorization header in all other queries and mutations.

To use this server, first fire up the docker-compose: (make sure its installed of course.) -->