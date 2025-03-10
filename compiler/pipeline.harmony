1. Source Code (.harmony)
    ↓
2. YAML IR (.yaml)
    ↓
3. JSON IR (.json)
    ↓
4. AST & H-IR (.hir)
    ↓
5. Machine Code (.exe / .bin)

project {
    name: "MyGame"
    type: "AAA"
    language: "Harmony-Code"
    version: "1.0"
    platform: ["Windows", "Linux"]
    frameworks: ["Unity", "Unreal"]
    buildTools: ["CMake"]
    debugMode: true
}

entity Player {
    health: int = 100
    score: int = 0

    function onStart() {
        print("Player has entered the game!")
    }

    function onUpdate() {
        score += 10
        print("Player's score: " + score)
    }
}

# Main Game Loop
gameLoop {
    onUpdate()
    onRender()
}

project:
  name: "MyGame"
  type: "AAA"
  language: "Harmony-Code"
  version: "1.0"
  platform:
    - "Windows"
    - "Linux"
  frameworks:
    - "Unity"
    - "Unreal"
  buildTools:
    - "CMake"
  debugMode: true

entities:
  Player:
    properties:
      - health: int = 100
      - score: int = 0
    methods:
      - onStart:
          body:
            - print("Player has entered the game!")
      - onUpdate:
          body:
            - score += 10
            - print("Player's score: " + score)

gameLoop:
  events:
    - onUpdate: {}
    - onRender: {}

{
    "project": {
        "name": "MyGame",
        "type": "AAA",
        "language": "Harmony-Code",
        "version": "1.0",
        "platform": ["Windows", "Linux"],
        "frameworks": ["Unity", "Unreal"],
        "buildTools": ["CMake"],
        "debugMode": true
    },
    "entities": {
        "Player": {
            "properties": [
                {"health": {"type": "int", "value": 100}},
                {"score": {"type": "int", "value": 0}}
            ],
            "methods": [
                {"onStart": {"body": ["print(\"Player has entered the game!\")"]}},
                {"onUpdate": {"body": ["score += 10", "print(\"Player's score: \" + score)"]}}
            ]
        }
    },
    "gameLoop": {
        "events": [
            {"onUpdate": {}},
            {"onRender": {}}
        ]
    }
}

{
    "ast": {
        "root": {
            "type": "Program",
            "body": [
                {
                    "type": "ProjectDeclaration",
                    "name": "MyGame",
                    "properties": {
                        "name": "MyGame",
                        "type": "AAA",
                        "language": "Harmony-Code",
                        "version": "1.0"
                    }
                },
                {
                    "type": "EntityDeclaration",
                    "name": "Player",
                    "properties": {
                        "health": { "type": "int", "value": 100 },
                        "score": { "type": "int", "value": 0 }
                    },
                    "methods": [
                        {
                            "type": "FunctionDeclaration",
                            "name": "onStart",
                            "body": [
                                {
                                    "type": "Expression",
                                    "value": "print('Player has entered the game!')"
                                }
                            ]
                        },
                        {
                            "type": "FunctionDeclaration",
                            "name": "onUpdate",
                            "body": [
                                { "type": "Expression", "value": "score += 10" },
                                { "type": "Expression", "value": "print('Player's score: ' + score)" }
                            ]
                        }
                    ]
                },
                {
                    "type": "GameLoopDeclaration",
                    "events": [
                        { "type": "Event", "name": "onUpdate" },
                        { "type": "Event", "name": "onRender" }
                    ]
                }
            ]
        }
    },
    "hir": {
        "functions": [
            {
                "name": "onStart",
                "operations": [
                    {"type": "print", "arguments": ["'Player has entered the game!'"]}
                ]
            },
            {
                "name": "onUpdate",
                "operations": [
                    {"type": "increment", "variable": "score", "value": 10},
                    {"type": "print", "arguments": ["'Player's score: ' + score"]}
                ]
            }
        ],
        "gameLoop": {
            "events": ["onUpdate", "onRender"]
        }
    }
}

