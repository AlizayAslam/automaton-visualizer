

# Automaton Visualizer
   A Python-based GUI application for creating, visualizing, and analyzing Deterministic Finite Automata (DFA) and Nondeterministic Finite Automata (NFA). Built with Tkinter, automata-lib, and Graphviz, this tool allows users to design automata, generate visual diagrams, test input strings, convert DFAs to NFAs, and minimize DFAs.
   
## Features

**Create DFA/NFA**: Define states, alphabet, transitions, initial state, and final states via a user-friendly GUI.
**Visualize Automata**: Generate PDF diagrams using Graphviz with customizable layout and colors.
**Test Inputs**: Trace input strings through the automaton and display acceptance results.
**Convert DFA to NFA**: Transform a DFA into an equivalent NFA.
**Minimize DFA**: Reduce a DFA to its minimal form.
**Input Validation**: Robust error checking for states, transitions, and input strings.
**Customizable UI**: Adjust diagram layout direction, state colors, and transition colors.


# Prerequisites

Python 3.6+
# Dependencies:
**automata-lib**: For DFA/NFA logic.
**graphviz**: For rendering automaton diagrams.
**tkinter**: For the GUI (usually included with Python).


# Graphviz: The Graphviz software must be installed on your system (not just the Python package).

# Installation
Clone the Repository:
https://github.com/AlizayAslam/automaton-visualizer.git
cd automaton-visualizer


# Install Python Dependencies:
pip install automata-lib graphviz

# GUI Instructions:

**Select Automaton Type**: Choose DFA or NFA.
## Enter Details:
States: Comma-separated list (e.g., q0,q1,q2).
Alphabet: Comma-separated symbols (e.g., a,b).
Initial State: Single state (e.g., q0).
Final States: Comma-separated list (e.g., q1,q2).
Transitions: Semicolon-separated triples (e.g., q0,a,q1;q0,b,q2).
Test Inputs: Comma-separated strings to test (e.g., a,ab,ba).
Customize Diagram: Choose layout direction (LR/TB) and colors for states and transitions.
Actions:
Generate Diagram: Creates a PDF diagram in ~/Desktop/AutomatonDiagrams/ (or current directory if access is denied).
Test Input Strings: Displays transition traces and acceptance results.
Convert DFA to NFA: Converts the current DFA to an equivalent NFA.
Minimize DFA: Reduces the DFA to its minimal form.
Clear Inputs: Resets all input fields.




# Output:

Diagrams are saved as PDFs in ~/Desktop/AutomatonDiagrams/ with unique filenames (e.g., dfa_diagram_<uuid>.pdf).
Results are displayed in the GUI’s text area.



Example
   DFA Example:

States: q0,q1,q2
Alphabet: 0,1
Initial State: q0
Final States: q1
Transitions: q0,0,q0;q0,1,q1;q1,0,q2;q1,1,q1;q2,0,q2;q2,1,q2
Test Inputs: 01,001,11

   Click "Generate Diagram" to visualize the DFA, or "Test Input Strings" to see the transition traces.

# Notes

NFA Support: Use epsilon for ε-transitions in NFA mode.
Error Handling: The app validates inputs and provides error messages for incorrect formats or incomplete DFAs.
Generated Files: PDFs and the AutomatonDiagrams folder are excluded from Git tracking via .gitignore.
Cross-Platform: Tested on Windows, Mac, and Linux (ensure Graphviz is installed).

# Troubleshooting

Graphviz Error: Ensure Graphviz is installed and its bin directory is in your PATH.
Permission Denied: If diagrams can’t save to Desktop, they’ll save to the current directory’s AutomatonDiagrams folder.
Invalid Inputs: Check error messages in the GUI for guidance on fixing input formats.

Contributing
   Contributions are welcome! Please submit a pull request or open an issue on GitHub.

**Aleeza Aslam**
