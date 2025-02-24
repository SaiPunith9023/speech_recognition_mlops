```mermaid
graph TD;
    A[User] -->|Gives Voice Command| B[Speech Recognition]
    B -->|Recognizes Command| C[Action Processor]
    C -->|Executes| D[Browser Control / Hardware Control / RPA]
    D -->|Response| E[Text-to-Speech]
    E -->|Audio Feedback| A
