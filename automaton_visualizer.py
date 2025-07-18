# import tkinter as tk
# from tkinter import messagebox, ttk
# from automata.fa.dfa import DFA
# from automata.fa.nfa import NFA
# from graphviz import Digraph, ExecutableNotFound
# import uuid
# import re

# class AutomatonVisualizerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Automaton Visualizer - Enhanced Edition")
#         self.root.geometry("900x700")
#         self.automaton_type = tk.StringVar(value="DFA")
#         self.transitions = {}
#         self.layout_direction = tk.StringVar(value="LR")
#         self.state_color = tk.StringVar(value="lightblue")
#         self.transition_color = tk.StringVar(value="black")
#         self.check_dependencies()
#         self.create_ui()

#     def check_dependencies(self):
#         """Check if required dependencies are installed."""
#         try:
#             import automata
#         except ImportError:
#             messagebox.showerror("Dependency Error", "Please install automata-lib: pip install automata-lib")
#             self.root.quit()
#         try:
#             Digraph().render('test', format='pdf', cleanup=True)
#         except ExecutableNotFound:
#             messagebox.showerror("Dependency Error", "Please install Graphviz from https://graphviz.org/")
#             self.root.quit()

#     def create_ui(self):
#         main_frame = tk.Frame(self.root, bg="white")
#         main_frame.pack(fill="both", expand=True)
#         canvas = tk.Canvas(main_frame, bg="white")
#         scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
#         scrollable_frame = tk.Frame(canvas, bg="white")
#         canvas.configure(yscrollcommand=scrollbar.set)
#         scrollbar.pack(side="right", fill="y")
#         canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0)
#         canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#         def on_frame_configure(event):
#             canvas.configure(scrollregion=canvas.bbox("all"))
#             canvas.itemconfig(canvas_window, width=canvas.winfo_width())
#         scrollable_frame.bind("<Configure>", on_frame_configure)
#         def on_mouse_wheel(event):
#             canvas.yview_scroll(-1 * (event.delta // 120), "units")
#         canvas.bind_all("<MouseWheel>", on_mouse_wheel)
#         self.title_label = tk.Label(
#             scrollable_frame,
#             text="Automaton Visualizer",
#             font=("Arial", 18, "bold"),
#             fg="#2E86C1",
#             bg="white"
#         )
#         self.title_label.pack(pady=(10, 5), anchor="w", padx=10)
#         self.pulsate_title()
#         type_frame = tk.Frame(scrollable_frame, bg="white")
#         type_frame.pack(fill="x", pady=5, padx=10)
#         tk.Label(type_frame, text="Select Automaton Type:", font=("Arial", 12, "bold"), bg="white").pack(side="left")
#         tk.Radiobutton(type_frame, text="DFA", variable=self.automaton_type, value="DFA", bg="white").pack(side="left", padx=10)
#         tk.Radiobutton(type_frame, text="NFA", variable=self.automaton_type, value="NFA", bg="white").pack(side="left")
#         input_container = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid")
#         input_container.pack(fill="x", padx=10, pady=5)
#         self.create_label_and_entry(input_container, "States (comma-separated, e.g., q0,q1,q2):", "states_entry", "Enter unique state names separated by commas")
#         self.create_label_and_entry(input_container, "Alphabet (comma-separated, e.g., a,b):", "alphabet_entry", "Enter input symbols separated by commas")
#         self.create_label_and_entry(input_container, "Initial State (e.g., q0):", "initial_entry", "Enter the starting state")
#         self.create_label_and_entry(input_container, "Final States (comma-separated, e.g., q1,q2):", "final_entry", "Enter accepting states separated by commas")
#         self.create_label_and_entry(input_container, "Transitions (e.g., q0,a,q1; q0,b,q1):", "transitions_entry", "Format: source,symbol,destination; multiple transitions separated by semicolons")
#         self.create_label_and_entry(input_container, "Test Input Strings (comma-separated, e.g., a,ab,ba):", "input_string_entry", "Enter strings to test the automaton")
#         epsilon_label = tk.Label(scrollable_frame, text="For NFA, use 'epsilon' for ε-transitions", bg="white", font=("Arial", 8))
#         epsilon_label.pack(anchor="w", padx=15, pady=2)
#         customization_frame = tk.Frame(scrollable_frame, bg="white")
#         customization_frame.pack(fill="x", pady=5, padx=10)
#         tk.Label(customization_frame, text="Diagram Customization:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
#         layout_frame = tk.Frame(scrollable_frame, bg="white")
#         layout_frame.pack(fill="x", padx=10, pady=2)
#         tk.Label(layout_frame, text="Layout Direction:", bg="white").pack(side="left")
#         layout_dropdown = tk.OptionMenu(layout_frame, self.layout_direction, "LR", "TB")
#         layout_dropdown.pack(side="left", padx=10)
#         state_color_frame = tk.Frame(scrollable_frame, bg="white")
#         state_color_frame.pack(fill="x", padx=10, pady=2)
#         tk.Label(state_color_frame, text="State Color:", bg="white").pack(side="left")
#         state_color_dropdown = tk.OptionMenu(state_color_frame, self.state_color, "lightblue", "lightgreen", "lightyellow", "lightcoral")
#         state_color_dropdown.pack(side="left", padx=10)
#         transition_color_frame = tk.Frame(scrollable_frame, bg="white")
#         transition_color_frame.pack(fill="x", padx=10, pady=2)
#         tk.Label(transition_color_frame, text="Transition Color:", bg="white").pack(side="left")
#         transition_color_dropdown = tk.OptionMenu(transition_color_frame, self.transition_color, "black", "blue", "red", "green")
#         transition_color_dropdown.pack(side="left", padx=10)
#         button_frame = tk.Frame(scrollable_frame, bg="white")
#         button_frame.pack(fill="x", pady=10, padx=10)
#         self.create_button(button_frame, "Generate Diagram", self.generate_diagram, "#2E86C1")
#         self.create_button(button_frame, "Test Input Strings", self.test_input, "#28B463")
#         self.create_button(button_frame, "Convert DFA to NFA", self.convert_dfa_to_nfa, "#8E44AD")
#         self.create_button(button_frame, "Minimize DFA", self.minimize_dfa, "#D35400")
#         self.create_button(button_frame, "Clear Inputs", self.clear_inputs, "#E74C3C")
#         results_frame = tk.Frame(scrollable_frame, bg="white")
#         results_frame.pack(fill="x", pady=5, padx=10)
#         tk.Label(results_frame, text="Results:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
#         result_frame = tk.Frame(results_frame, bg="white")
#         result_frame.pack(fill="x")
#         self.result_text = tk.Text(result_frame, height=12, width=70, relief="solid", bd=1, font=("Arial", 10))
#         result_scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
#         self.result_text.configure(yscrollcommand=result_scrollbar.set)
#         self.result_text.pack(side="left", fill="x", expand=True)
#         result_scrollbar.pack(side="right", fill="y")

#     def create_label_and_entry(self, parent, text, attr_name, tooltip):
#         frame = tk.Frame(parent, bg="white")
#         frame.pack(fill="x", padx=5, pady=3)
#         tk.Label(frame, text=text, bg="white", width=30, anchor="w").pack(side="left")
#         entry = tk.Entry(frame, width=50, relief="solid", bd=1)
#         entry.pack(side="left", fill="x", expand=True, padx=5)
#         setattr(self, attr_name, entry)
#         self.create_tooltip(entry, tooltip)

#     def create_button(self, parent, text, command, color):
#         btn = tk.Button(
#             parent,
#             text=text,
#             command=command,
#             bg=color,
#             fg="white",
#             font=("Arial", 10, "bold"),
#             relief="flat",
#             padx=10,
#             pady=5
#         )
#         btn.pack(side="left", padx=5)

#     def create_tooltip(self, widget, text):
#         def enter(event):
#             if not hasattr(self, 'tooltip'):
#                 x, y, _, _ = widget.bbox("insert")
#                 x += widget.winfo_rootx() + 25
#                 y += widget.winfo_rooty() + 25
#                 self.tooltip = tk.Toplevel(widget)
#                 self.tooltip.wm_overrideredirect(True)
#                 self.tooltip.wm_geometry(f"+{x}+{y}")
#                 label = tk.Label(self.tooltip, text=text, bg="lightyellow", relief="solid", borderwidth=1)
#                 label.pack()
#         def leave(event):
#             if hasattr(self, 'tooltip'):
#                 self.tooltip.destroy()
#                 del self.tooltip
#         widget.bind("<Enter>", enter)
#         widget.bind("<Leave>", leave)

#     def pulsate_title(self):
#         current_color = self.title_label.cget("fg")
#         r, g, b = int(current_color[1:3], 16), int(current_color[3:5], 16), int(current_color[5:7], 16)
#         if r > 100:
#             r, g, b = max(46, r - 10), max(134, g - 10), max(193, b - 10)
#         else:
#             r, g, b = min(46, r + 10), min(134, g + 10), min(193, b + 10)
#         new_color = f"#{r:02x}{g:02x}{b:02x}"
#         self.title_label.config(fg=new_color)
#         self.root.after(200, self.pulsate_title)

#     def clear_inputs(self):
#         for field in ['states_entry', 'alphabet_entry', 'initial_entry', 'final_entry', 'transitions_entry', 'input_string_entry']:
#             getattr(self, field).delete(0, tk.END)
#         self.result_text.delete(1.0, tk.END)
#         self.automaton_type.set("DFA")
#         self.layout_direction.set("LR")
#         self.state_color.set("lightblue")
#         self.transition_color.set("black")

#     def parse_states(self, states_input):
#         """Parse and validate states input."""
#         if not states_input or not states_input.strip():
#             raise ValueError("States cannot be empty")
#         states = set(s.strip() for s in states_input.split(",") if s.strip())
#         if not states:
#             raise ValueError("No valid states provided")
#         if any(not re.match(r"^[a-zA-Z0-9_]+$", s) for s in states):
#             raise ValueError("States can only contain alphanumeric characters or underscores")
#         return states

#     def parse_alphabet(self, alphabet_input):
#         """Parse and validate alphabet input."""
#         if not alphabet_input or not alphabet_input.strip():
#             raise ValueError("Alphabet cannot be empty")
#         alphabet = set(a.strip() for a in alphabet_input.split(",") if a.strip())
#         if not alphabet:
#             raise ValueError("No valid alphabet symbols provided")
#         if any(not re.match(r"^[a-zA-Z0-9_]+$", a) for a in alphabet):
#             raise ValueError("Alphabet symbols can only contain alphanumeric characters or underscores")
#         if self.automaton_type.get() == "NFA":
#             alphabet.add("epsilon")
#         return alphabet

#     def parse_initial_state(self, initial_state_input, states):
#         """Parse and validate initial state input."""
#         if not initial_state_input or not initial_state_input.strip():
#             raise ValueError("Initial state cannot be empty")
#         initial_state = initial_state_input.strip()
#         if initial_state not in states:
#             raise ValueError(f"Initial state '{initial_state}' not in states")
#         return initial_state

#     def parse_final_states(self, final_states_input, states):
#         """Parse and validate final states input."""
#         final_states = set(f.strip() for f in final_states_input.split(",") if f.strip()) if final_states_input.strip() else set()
#         for f in final_states:
#             if f not in states:
#                 raise ValueError(f"Final state '{f}' not in states")
#         return final_states

#     def parse_transitions(self, transitions_input, states, alphabet):
#         """Parse and validate transitions input."""
#         if not transitions_input or not transitions_input.strip():
#             raise ValueError("Transitions cannot be empty")
#         self.transitions = {state: {} for state in states}
#         for line in transitions_input.split(";"):
#             if line.strip():
#                 parts = [p.strip() for p in line.split(",")]
#                 if len(parts) != 3:
#                     raise ValueError(f"Invalid transition format: {line}")
#                 src, symbol, dst = parts
#                 if src not in states or dst not in states:
#                     raise ValueError(f"Transition involves undeclared state: {src} or {dst}")
#                 if symbol not in alphabet:
#                     raise ValueError(f"Symbol '{symbol}' not in alphabet")
#                 if self.automaton_type.get() == "DFA" and symbol == "epsilon":
#                     raise ValueError("Epsilon transitions are not allowed in DFA")
#                 if self.automaton_type.get() == "DFA":
#                     if symbol in self.transitions[src]:
#                         raise ValueError(f"DFA cannot have multiple transitions for state '{src}' on symbol '{symbol}'")
#                     self.transitions[src][symbol] = {dst}
#                 else:
#                     if symbol not in self.transitions[src]:
#                         self.transitions[src][symbol] = set()
#                     self.transitions[src][symbol].add(dst)
#         if self.automaton_type.get() == "DFA":
#             for state in states:
#                 for symbol in alphabet:
#                     if symbol not in self.transitions.get(state, {}):
#                         raise ValueError(f"DFA incomplete: No transition defined for state '{state}' on symbol '{symbol}'")
#         return self.transitions

#     def parse_inputs(self):
#         """Parse and validate all inputs."""
#         states = self.parse_states(self.states_entry.get())
#         alphabet = self.parse_alphabet(self.alphabet_entry.get())
#         initial_state = self.parse_initial_state(self.initial_entry.get(), states)
#         final_states = self.parse_final_states(self.final_entry.get(), states)
#         self.parse_transitions(self.transitions_entry.get(), states, alphabet)
#         return states, alphabet, initial_state, final_states

#     def convert_dfa_to_nfa(self):
#         try:
#             if self.automaton_type.get() != "DFA":
#                 raise ValueError("Conversion to NFA is only applicable for DFA")
#             states, alphabet, initial_state, final_states = self.parse_inputs()
#             nfa_transitions = {state: {symbol: trans[symbol] for symbol in trans} for state, trans in self.transitions.items()}
#             nfa = NFA(
#                 states=states,
#                 input_symbols=alphabet - {"epsilon"},
#                 transitions=nfa_transitions,
#                 initial_state=initial_state,
#                 final_states=final_states
#             )
#             self.automaton_type.set("NFA")
#             self.result_text.delete(1.0, tk.END)
#             self.result_text.insert(tk.END, "Converted DFA to NFA:\n")
#             self.result_text.insert(tk.END, f"States: {', '.join(states)}\n")
#             self.result_text.insert(tk.END, f"Alphabet: {', '.join(alphabet - {'epsilon'})}\n")
#             self.result_text.insert(tk.END, f"Initial State: {initial_state}\n")
#             self.result_text.insert(tk.END, f"Final States: {', '.join(final_states)}\n")
#             self.result_text.insert(tk.END, "Transitions:\n")
#             for src, trans in nfa_transitions.items():
#                 for symbol, dsts in trans.items():
#                     for dst in dsts:
#                         self.result_text.insert(tk.END, f"  {src} --{symbol}--> {dst}\n")
#             messagebox.showinfo("Success", "DFA converted to NFA. You can now generate the NFA diagram or test inputs.")
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#         except Exception as e:
#             messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

#     def minimize_dfa(self):
#         try:
#             if self.automaton_type.get() != "DFA":
#                 raise ValueError("Minimization is only applicable for DFA")
#             states, alphabet, initial_state, final_states = self.parse_inputs()
#             dfa_transitions = {state: {symbol: next(iter(trans[symbol])) for symbol in trans} for state, trans in self.transitions.items()}
#             dfa = DFA(
#                 states=states,
#                 input_symbols=alphabet,
#                 transitions=dfa_transitions,
#                 initial_state=initial_state,
#                 final_states=final_states
#             )
#             # Compute reachable states
#             reachable_states = set()
#             stack = [initial_state]
#             while stack:
#                 state = stack.pop()
#                 if state not in reachable_states:
#                     reachable_states.add(state)
#                     for symbol in alphabet:
#                         if symbol in dfa_transitions.get(state, {}):
#                             stack.append(dfa_transitions[state][symbol])
#             # Partition refinement algorithm for DFA minimization
#             non_final_states = reachable_states - final_states
#             partitions = [final_states, non_final_states] if non_final_states else [final_states]
#             changed = True
#             while changed:
#                 changed = False
#                 new_partitions = []
#                 for partition in partitions:
#                     if len(partition) <= 1:
#                         new_partitions.append(partition)
#                         continue
#                     groups = {}
#                     for state in partition:
#                         signature = tuple(
#                             next((i for i, p in enumerate(partitions) if dfa_transitions[state][symbol] in p), -1)
#                             if symbol in dfa_transitions[state] else -1
#                             for symbol in alphabet
#                         )
#                         if signature not in groups:
#                             groups[signature] = set()
#                         groups[signature].add(state)
#                     for group in groups.values():
#                         new_partitions.append(group)
#                         if len(group) < len(partition):
#                             changed = True
#                 partitions = new_partitions
#             state_map = {state: next(iter(partition)) for partition in partitions for state in partition}
#             min_states = set(state_map[state] for state in reachable_states)
#             min_final_states = set(state_map[state] for state in final_states if state in reachable_states)
#             min_initial_state = state_map[initial_state]
#             min_transitions = {}
#             for state in min_states:
#                 min_transitions[state] = {}
#                 orig_state = next(s for s in reachable_states if state_map[s] == state)
#                 for symbol in alphabet:
#                     if symbol in dfa_transitions.get(orig_state, {}):
#                         min_transitions[state][symbol] = state_map[dfa_transitions[orig_state][symbol]]
#             self.states_entry.delete(0, tk.END)
#             self.states_entry.insert(0, ",".join(min_states))
#             self.initial_entry.delete(0, tk.END)
#             self.initial_entry.insert(0, min_initial_state)
#             self.final_entry.delete(0, tk.END)
#             self.final_entry.insert(0, ",".join(min_final_states))
#             self.transitions_entry.delete(0, tk.END)
#             trans_str = ";".join(f"{src},{symbol},{dst}" for src, trans in min_transitions.items() for symbol, dst in trans.items())
#             self.transitions_entry.insert(0, trans_str)
#             self.result_text.delete(1.0, tk.END)
#             self.result_text.insert(tk.END, "Minimized DFA:\n")
#             self.result_text.insert(tk.END, f"States: {', '.join(min_states)}\n")
#             self.result_text.insert(tk.END, f"Alphabet: {', '.join(alphabet)}\n")
#             self.result_text.insert(tk.END, f"Initial State: {min_initial_state}\n")
#             self.result_text.insert(tk.END, f"Final States: {', '.join(min_final_states)}\n")
#             self.result_text.insert(tk.END, "Transitions:\n")
#             for src, trans in min_transitions.items():
#                 for symbol, dst in trans.items():
#                     self.result_text.insert(tk.END, f"  {src} --{symbol}--> {dst}\n")
#             messagebox.showinfo("Success", "DFA minimized. Input fields updated with minimized DFA. You can now generate the diagram or test inputs.")
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#         except Exception as e:
#             messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

#     def generate_diagram(self):
#         try:
#             states, alphabet, initial_state, final_states = self.parse_inputs()
#             dot = Digraph(comment="Automaton Diagram")
#             dot.attr(rankdir=self.layout_direction.get())
#             dot.attr('node', fontsize='12')
#             dot.attr('edge', fontsize='10')
#             for state in states:
#                 style = "doublecircle" if state in final_states else "circle"
#                 dot.node(state, shape=style, style="filled", fillcolor=self.state_color.get())
#             dot.node("start", shape="none", label="")
#             dot.edge("start", initial_state, color=self.transition_color.get())
#             if self.automaton_type.get() == "NFA":
#                 edge_labels = {}
#                 for src, trans in self.transitions.items():
#                     for symbol, dsts in trans.items():
#                         for dst in dsts:
#                             edge_key = (src, dst)
#                             label = "ε" if symbol == "epsilon" else symbol
#                             if edge_key not in edge_labels:
#                                 edge_labels[edge_key] = set()
#                             edge_labels[edge_key].add(label)
#                 for (src, dst), labels in edge_labels.items():
#                     combined_label = ",".join(sorted(labels))
#                     dot.edge(src, dst, label=combined_label, color=self.transition_color.get())
#             else:
#                 edge_labels = {}
#                 for src, trans in self.transitions.items():
#                     for symbol, dsts in trans.items():
#                         for dst in dsts:
#                             edge_key = (src, dst)
#                             label = "ε" if symbol == "epsilon" else symbol
#                             if edge_key not in edge_labels:
#                                 edge_labels[edge_key] = set()
#                             edge_labels[edge_key].add(label)
#                 for (src, dst), labels in edge_labels.items():
#                     combined_label = ",".join(sorted(labels))
#                     dot.edge(src, dst, label=combined_label, color=self.transition_color.get())
#             filename = f"{'dfa' if self.automaton_type.get() == 'DFA' else 'nfa'}_diagram_{uuid.uuid4().hex}"
#             dot.render(filename, format="pdf", view=True, cleanup=True)
#             messagebox.showinfo("Success", f"Diagram generated and saved as {filename}.pdf!")
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#         except ExecutableNotFound:
#             messagebox.showerror("Error", "Graphviz executable not found. Please install Graphviz from https://graphviz.org/")
#         except Exception as e:
#             messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

#     def get_epsilon_closure(self, states, transitions):
#         """Compute the epsilon closure of a set of states for NFA."""
#         closure = set(states)
#         stack = list(states)
#         while stack:
#             state = stack.pop()
#             if "epsilon" in transitions.get(state, {}):
#                 for next_state in transitions[state]["epsilon"]:
#                     if next_state not in closure:
#                         closure.add(next_state)
#                         stack.append(next_state)
#         return closure

#     def trace_transitions(self, automaton, input_string, states, initial_state, final_states):
#         """Trace the state transitions for an input string."""
#         current_states = {initial_state}
#         if isinstance(automaton, NFA):
#             current_states = self.get_epsilon_closure(current_states, automaton.transitions)
#         trace = [f"Start: {current_states}"]
#         for symbol in input_string:
#             next_states = set()
#             for state in current_states:
#                 if isinstance(automaton, DFA):
#                     if symbol in automaton.transitions.get(state, {}):
#                         next_states.add(list(automaton.transitions[state][symbol])[0])
#                 else:
#                     if symbol in automaton.transitions.get(state, {}):
#                         next_states.update(automaton.transitions[state][symbol])
#             if isinstance(automaton, NFA):
#                 next_states = self.get_epsilon_closure(next_states, automaton.transitions)
#             current_states = next_states
#             trace.append(f"On '{symbol}': {current_states}")
#         accepted = bool(current_states & final_states)
#         trace.append(f"End: {current_states}, Accepted: {accepted}")
#         return trace, accepted

#     def test_input(self):
#         try:
#             states, alphabet, initial_state, final_states = self.parse_inputs()
#             inputs = [s.strip() for s in self.input_string_entry.get().split(",") if s.strip()]
#             if not inputs:
#                 raise ValueError("No input strings provided")
#             if self.automaton_type.get() == "DFA":
#                 transitions = {state: {symbol: next(iter(dest)) for symbol, dest in trans.items()} for state, trans in self.transitions.items()}
#                 automaton = DFA(
#                     states=states,
#                     input_symbols=alphabet - {"epsilon"},
#                     transitions=transitions,
#                     initial_state=initial_state,
#                     final_states=final_states
#                 )
#             else:
#                 automaton = NFA(
#                     states=states,
#                     input_symbols=alphabet - {"epsilon"},
#                     transitions=self.transitions,
#                     initial_state=initial_state,
#                     final_states=final_states
#                 )
#             self.result_text.delete(1.0, tk.END)
#             for inp in inputs:
#                 if any(c not in alphabet - {"epsilon"} for c in inp):
#                     self.result_text.insert(tk.END, f"Input '{inp}' contains invalid symbols\n\n")
#                     continue
#                 trace, accepted = self.trace_transitions(automaton, inp, states, initial_state, final_states)
#                 self.result_text.insert(tk.END, f"Trace for input '{inp}':\n" + "\n".join(trace) + "\n\n")
#         except ValueError as e:
#             messagebox.showerror("Error", str(e))
#         except Exception as e:
#             messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = AutomatonVisualizerApp(root)
#     root.mainloop()
import tkinter as tk
from tkinter import messagebox, ttk
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from graphviz import Digraph, ExecutableNotFound
import uuid
import re
import os

class AutomatonVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automaton Visualizer - Enhanced Edition")
        self.root.geometry("900x700")
        self.automaton_type = tk.StringVar(value="DFA")
        self.transitions = {}
        self.layout_direction = tk.StringVar(value="LR")
        self.state_color = tk.StringVar(value="lightblue")
        self.transition_color = tk.StringVar(value="black")
        self.check_dependencies()
        self.create_ui()

    def check_dependencies(self):
        """Check if required dependencies are installed."""
        try:
            import automata
        except ImportError:
            messagebox.showerror("Dependency Error", "Please install automata-lib: pip install automata-lib")
            self.root.quit()
        try:
            Digraph().render('test', format='pdf', cleanup=True)
        except ExecutableNotFound:
            messagebox.showerror("Dependency Error", "Please install Graphviz from https://graphviz.org/")
            self.root.quit()

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=0, pady=0)
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(canvas_window, width=canvas.winfo_width())
        scrollable_frame.bind("<Configure>", on_frame_configure)
        def on_mouse_wheel(event):
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        self.title_label = tk.Label(
            scrollable_frame,
            text="Automaton Visualizer",
            font=("Arial", 18, "bold"),
            fg="#2E86C1",
            bg="white"
        )
        self.title_label.pack(pady=(10, 5), anchor="w", padx=10)
        self.pulsate_title()
        type_frame = tk.Frame(scrollable_frame, bg="white")
        type_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(type_frame, text="Select Automaton Type:", font=("Arial", 12, "bold"), bg="white").pack(side="left")
        tk.Radiobutton(type_frame, text="DFA", variable=self.automaton_type, value="DFA", bg="white").pack(side="left", padx=10)
        tk.Radiobutton(type_frame, text="NFA", variable=self.automaton_type, value="NFA", bg="white").pack(side="left")
        input_container = tk.Frame(scrollable_frame, bg="white", bd=1, relief="solid")
        input_container.pack(fill="x", padx=10, pady=5)
        self.create_label_and_entry(input_container, "States (comma-separated, e.g., q0,q1,q2):", "states_entry", "Enter unique state names separated by commas")
        self.create_label_and_entry(input_container, "Alphabet (comma-separated, e.g., a,b):", "alphabet_entry", "Enter input symbols separated by commas")
        self.create_label_and_entry(input_container, "Initial State (e.g., q0):", "initial_entry", "Enter the starting state")
        self.create_label_and_entry(input_container, "Final States (comma-separated, e.g., q1,q2):", "final_entry", "Enter accepting states separated by commas")
        self.create_label_and_entry(input_container, "Transitions (e.g., q0,a,q1; q0,b,q1):", "transitions_entry", "Format: source,symbol,destination; multiple transitions separated by semicolons")
        self.create_label_and_entry(input_container, "Test Input Strings (comma-separated, e.g., a,ab,ba):", "input_string_entry", "Enter strings to test the automaton")
        epsilon_label = tk.Label(scrollable_frame, text="For NFA, use 'epsilon' for ε-transitions", bg="white", font=("Arial", 8))
        epsilon_label.pack(anchor="w", padx=15, pady=2)
        customization_frame = tk.Frame(scrollable_frame, bg="white")
        customization_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(customization_frame, text="Diagram Customization:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        layout_frame = tk.Frame(scrollable_frame, bg="white")
        layout_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(layout_frame, text="Layout Direction:", bg="white").pack(side="left")
        layout_dropdown = tk.OptionMenu(layout_frame, self.layout_direction, "LR", "TB")
        layout_dropdown.pack(side="left", padx=10)
        state_color_frame = tk.Frame(scrollable_frame, bg="white")
        state_color_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(state_color_frame, text="State Color:", bg="white").pack(side="left")
        state_color_dropdown = tk.OptionMenu(state_color_frame, self.state_color, "lightblue", "lightgreen", "lightyellow", "lightcoral")
        state_color_dropdown.pack(side="left", padx=10)
        transition_color_frame = tk.Frame(scrollable_frame, bg="white")
        transition_color_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(transition_color_frame, text="Transition Color:", bg="white").pack(side="left")
        transition_color_dropdown = tk.OptionMenu(transition_color_frame, self.transition_color, "black", "blue", "red", "green")
        transition_color_dropdown.pack(side="left", padx=10)
        button_frame = tk.Frame(scrollable_frame, bg="white")
        button_frame.pack(fill="x", pady=10, padx=10)
        self.create_button(button_frame, "Generate Diagram", self.generate_diagram, "#2E86C1")
        self.create_button(button_frame, "Test Input Strings", self.test_input, "#28B463")
        self.create_button(button_frame, "Convert DFA to NFA", self.convert_dfa_to_nfa, "#8E44AD")
        self.create_button(button_frame, "Minimize DFA", self.minimize_dfa, "#D35400")
        self.create_button(button_frame, "Clear Inputs", self.clear_inputs, "#E74C3C")
        results_frame = tk.Frame(scrollable_frame, bg="white")
        results_frame.pack(fill="x", pady=5, padx=10)
        tk.Label(results_frame, text="Results:", font=("Arial", 12, "bold"), bg="white").pack(anchor="w")
        result_frame = tk.Frame(results_frame, bg="white")
        result_frame.pack(fill="x")
        self.result_text = tk.Text(result_frame, height=20, width=70, relief="solid", bd=1, font=("Arial", 10))  # Increased height to 20
        result_scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=result_scrollbar.set)
        self.result_text.pack(side="left", fill="both", expand=True)
        result_scrollbar.pack(side="right", fill="y")

    def create_label_and_entry(self, parent, text, attr_name, tooltip):
        frame = tk.Frame(parent, bg="white")
        frame.pack(fill="x", padx=5, pady=3)
        tk.Label(frame, text=text, bg="white", width=30, anchor="w").pack(side="left")
        entry = tk.Entry(frame, width=50, relief="solid", bd=1)
        entry.pack(side="left", fill="x", expand=True, padx=5)
        setattr(self, attr_name, entry)
        self.create_tooltip(entry, tooltip)

    def create_button(self, parent, text, command, color):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            padx=10,
            pady=5
        )
        btn.pack(side="left", padx=5)

    def create_tooltip(self, widget, text):
        def enter(event):
            if not hasattr(self, 'tooltip'):
                x, y, _, _ = widget.bbox("insert")
                x += widget.winfo_rootx() + 25
                y += widget.winfo_rooty() + 25
                self.tooltip = tk.Toplevel(widget)
                self.tooltip.wm_overrideredirect(True)
                self.tooltip.wm_geometry(f"+{x}+{y}")
                label = tk.Label(self.tooltip, text=text, bg="lightyellow", relief="solid", borderwidth=1)
                label.pack()
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                del self.tooltip
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def pulsate_title(self):
        current_color = self.title_label.cget("fg")
        r, g, b = int(current_color[1:3], 16), int(current_color[3:5], 16), int(current_color[5:7], 16)
        if r > 100:
            r, g, b = max(46, r - 10), max(134, g - 10), max(193, b - 10)
        else:
            r, g, b = min(46, r + 10), min(134, g + 10), min(193, b + 10)
        new_color = f"#{r:02x}{g:02x}{b:02x}"
        self.title_label.config(fg=new_color)
        self.root.after(200, self.pulsate_title)

    def clear_inputs(self):
        for field in ['states_entry', 'alphabet_entry', 'initial_entry', 'final_entry', 'transitions_entry', 'input_string_entry']:
            getattr(self, field).delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.automaton_type.set("DFA")
        self.layout_direction.set("LR")
        self.state_color.set("lightblue")
        self.transition_color.set("black")

    def parse_states(self, states_input):
        """Parse and validate states input."""
        if not states_input or not states_input.strip():
            raise ValueError("States cannot be empty")
        states = set(s.strip() for s in states_input.split(",") if s.strip())
        if not states:
            raise ValueError("No valid states provided")
        if any(not re.match(r"^[a-zA-Z0-9_]+$", s) for s in states):
            raise ValueError("States can only contain alphanumeric characters or underscores")
        return states

    def parse_alphabet(self, alphabet_input):
        """Parse and validate alphabet input."""
        if not alphabet_input or not alphabet_input.strip():
            raise ValueError("Alphabet cannot be empty")
        alphabet = set(a.strip() for a in alphabet_input.split(",") if a.strip())
        if not alphabet:
            raise ValueError("No valid alphabet symbols provided")
        if any(not re.match(r"^[a-zA-Z0-9_]+$", a) for a in alphabet):
            raise ValueError("Alphabet symbols can only contain alphanumeric characters or underscores")
        if self.automaton_type.get() == "NFA":
            alphabet.add("epsilon")
        return alphabet

    def parse_initial_state(self, initial_state_input, states):
        """Parse and validate initial state input."""
        if not initial_state_input or not initial_state_input.strip():
            raise ValueError("Initial state cannot be empty")
        initial_state = initial_state_input.strip()
        if initial_state not in states:
            raise ValueError(f"Initial state '{initial_state}' not in states")
        return initial_state

    def parse_final_states(self, final_states_input, states):
        """Parse and validate final states input."""
        final_states = set(f.strip() for f in final_states_input.split(",") if f.strip()) if final_states_input.strip() else set()
        for f in final_states:
            if f not in states:
                raise ValueError(f"Final state '{f}' not in states")
        return final_states

    def parse_transitions(self, transitions_input, states, alphabet):
        """Parse and validate transitions input."""
        if not transitions_input or not transitions_input.strip():
            raise ValueError("Transitions cannot be empty")
        self.transitions = {state: {} for state in states}
        for line in transitions_input.split(";"):
            line = line.strip()
            if line:
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 3:
                    raise ValueError(f"Invalid transition format: '{line}' (expected: source,symbol,destination)")
                src, symbol, dst = parts
                if src not in states:
                    raise ValueError(f"Source state '{src}' not in states {states}")
                if dst not in states:
                    raise ValueError(f"Destination state '{dst}' not in states {states}")
                if symbol not in alphabet:
                    raise ValueError(f"Symbol '{symbol}' not in alphabet {alphabet}")
                if self.automaton_type.get() == "DFA" and symbol == "epsilon":
                    raise ValueError("Epsilon transitions are not allowed in DFA")
                if self.automaton_type.get() == "DFA":
                    if symbol in self.transitions[src]:
                        raise ValueError(f"DFA cannot have multiple transitions for state '{src}' on symbol '{symbol}'")
                    self.transitions[src][symbol] = {dst}
                else:
                    if symbol not in self.transitions[src]:
                        self.transitions[src][symbol] = set()
                    self.transitions[src][symbol].add(dst)
        if self.automaton_type.get() == "DFA":
            for state in states:
                for symbol in alphabet:
                    if symbol not in self.transitions.get(state, {}):
                        raise ValueError(f"DFA incomplete: No transition defined for state '{state}' on symbol '{symbol}'")
        print("Parsed Transitions:", self.transitions)  # Debug
        return self.transitions

    def parse_inputs(self):
        """Parse all inputs from the GUI entries."""
        states = self.parse_states(self.states_entry.get())
        alphabet = self.parse_alphabet(self.alphabet_entry.get())
        initial_state = self.parse_initial_state(self.initial_entry.get(), states)
        final_states = self.parse_final_states(self.final_entry.get(), states)
        self.parse_transitions(self.transitions_entry.get(), states, alphabet)
        return states, alphabet, initial_state, final_states

    def convert_dfa_to_nfa(self):
        try:
            if self.automaton_type.get() != "DFA":
                raise ValueError("Conversion to NFA is only applicable for DFA")
            states, alphabet, initial_state, final_states = self.parse_inputs()
            nfa_transitions = {state: {symbol: trans[symbol] for symbol in trans} for state, trans in self.transitions.items()}
            nfa = NFA(
                states=states,
                input_symbols=alphabet - {"epsilon"},
                transitions=nfa_transitions,
                initial_state=initial_state,
                final_states=final_states
            )
            self.automaton_type.set("NFA")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Converted DFA to NFA:\n")
            self.result_text.insert(tk.END, f"States: {', '.join(states)}\n")
            self.result_text.insert(tk.END, f"Alphabet: {', '.join(alphabet - {'epsilon'})}\n")
            self.result_text.insert(tk.END, f"Initial State: {initial_state}\n")
            self.result_text.insert(tk.END, f"Final States: {', '.join(final_states)}\n")
            self.result_text.insert(tk.END, "Transitions:\n")
            for src, trans in nfa_transitions.items():
                for symbol, dsts in trans.items():
                    for dst in dsts:
                        self.result_text.insert(tk.END, f"  {src} --{symbol}--> {dst}\n")
            messagebox.showinfo("Success", "DFA converted to NFA. You can now generate the NFA diagram or test inputs.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

    def minimize_dfa(self):
        try:
            if self.automaton_type.get() != "DFA":
                raise ValueError("Minimization is only applicable for DFA")
            states, alphabet, initial_state, final_states = self.parse_inputs()
            dfa_transitions = {state: {symbol: next(iter(trans[symbol])) for symbol in trans} for state, trans in self.transitions.items()}
            dfa = DFA(
                states=states,
                input_symbols=alphabet,
                transitions=dfa_transitions,
                initial_state=initial_state,
                final_states=final_states
            )
            reachable_states = set()
            stack = [initial_state]
            while stack:
                state = stack.pop()
                if state not in reachable_states:
                    reachable_states.add(state)
                    for symbol in alphabet:
                        if symbol in dfa_transitions.get(state, {}):
                            stack.append(dfa_transitions[state][symbol])
            non_final_states = reachable_states - final_states
            partitions = [final_states, non_final_states] if non_final_states else [final_states]
            changed = True
            while changed:
                changed = False
                new_partitions = []
                for partition in partitions:
                    if len(partition) <= 1:
                        new_partitions.append(partition)
                        continue
                    groups = {}
                    for state in partition:
                        signature = tuple(
                            next((i for i, p in enumerate(partitions) if dfa_transitions[state][symbol] in p), -1)
                            if symbol in dfa_transitions[state] else -1
                            for symbol in alphabet
                        )
                        if signature not in groups:
                            groups[signature] = set()
                        groups[signature].add(state)
                    for group in groups.values():
                        new_partitions.append(group)
                        if len(group) < len(partition):
                            changed = True
                partitions = new_partitions
            state_map = {state: next(iter(partition)) for partition in partitions for state in partition}
            min_states = set(state_map[state] for state in reachable_states)
            min_final_states = set(state_map[state] for state in final_states if state in reachable_states)
            min_initial_state = state_map[initial_state]
            min_transitions = {}
            for state in min_states:
                min_transitions[state] = {}
                orig_state = next(s for s in reachable_states if state_map[s] == state)
                for symbol in alphabet:
                    if symbol in dfa_transitions.get(orig_state, {}):
                        min_transitions[state][symbol] = state_map[dfa_transitions[orig_state][symbol]]
            self.states_entry.delete(0, tk.END)
            self.states_entry.insert(0, ",".join(min_states))
            self.initial_entry.delete(0, tk.END)
            self.initial_entry.insert(0, min_initial_state)
            self.final_entry.delete(0, tk.END)
            self.final_entry.insert(0, ",".join(min_final_states))
            self.transitions_entry.delete(0, tk.END)
            trans_str = ";".join(f"{src},{symbol},{dst}" for src, trans in min_transitions.items() for symbol, dst in trans.items())
            self.transitions_entry.insert(0, trans_str)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Minimized DFA:\n")
            self.result_text.insert(tk.END, f"States: {', '.join(min_states)}\n")
            self.result_text.insert(tk.END, f"Alphabet: {', '.join(alphabet)}\n")
            self.result_text.insert(tk.END, f"Initial State: {min_initial_state}\n")
            self.result_text.insert(tk.END, f"Final States: {', '.join(min_final_states)}\n")
            self.result_text.insert(tk.END, "Transitions:\n")
            for src, trans in min_transitions.items():
                for symbol, dst in trans.items():
                    self.result_text.insert(tk.END, f"  {src} --{symbol}--> {dst}\n")
            messagebox.showinfo("Success", "DFA minimized. Input fields updated with minimized DFA. You can now generate the diagram or test inputs.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

    def generate_diagram(self):
        try:
            states, alphabet, initial_state, final_states = self.parse_inputs()
            dot = Digraph(comment="Automaton Diagram")
            dot.attr(rankdir=self.layout_direction.get())
            dot.attr('node', fontsize='12')
            dot.attr('edge', fontsize='10')
            for state in states:
                style = "doublecircle" if state in final_states else "circle"
                dot.node(state, shape=style, style="filled", fillcolor=self.state_color.get())
            dot.node("start", shape="none", label="")
            dot.edge("start", initial_state, color=self.transition_color.get())
            if self.automaton_type.get() == "NFA":
                edge_labels = {}
                for src, trans in self.transitions.items():
                    for symbol, dsts in trans.items():
                        for dst in dsts:
                            edge_key = (src, dst)
                            label = "ε" if symbol == "epsilon" else symbol
                            if edge_key not in edge_labels:
                                edge_labels[edge_key] = set()
                            edge_labels[edge_key].add(label)
                for (src, dst), labels in edge_labels.items():
                    combined_label = ",".join(sorted(labels))
                    dot.edge(src, dst, label=combined_label, color=self.transition_color.get())
            else:
                edge_labels = {}
                for src, trans in self.transitions.items():
                    for symbol, dsts in trans.items():
                        for dst in dsts:
                            edge_key = (src, dst)
                            label = "ε" if symbol == "epsilon" else symbol
                            if edge_key not in edge_labels:
                                edge_labels[edge_key] = set()
                            edge_labels[edge_key].add(label)
                for (src, dst), labels in edge_labels.items():
                    combined_label = ",".join(sorted(labels))
                    dot.edge(src, dst, label=combined_label, color=self.transition_color.get())
            # Dynamically determine desktop path
            custom_dir = os.path.join(os.path.expanduser("~"), "Desktop", "AutomatonDiagrams")
            try:
                os.makedirs(custom_dir, exist_ok=True)
            except PermissionError:
                # Fallback to current working directory if desktop access is denied
                custom_dir = os.path.join(os.getcwd(), "AutomatonDiagrams")
                os.makedirs(custom_dir, exist_ok=True)
                messagebox.showwarning("Permission Warning", f"Access denied to Desktop. Saving to {custom_dir} instead.")
            filename = os.path.join(custom_dir, f"{'dfa' if self.automaton_type.get() == 'DFA' else 'nfa'}_diagram_{uuid.uuid4().hex}")
            dot.render(filename, format="pdf", view=True, cleanup=True)
            messagebox.showinfo("Success", f"Diagram generated and saved as {filename}.pdf!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except ExecutableNotFound:
            messagebox.showerror("Error", "Graphviz executable not found. Please install Graphviz from https://graphviz.org/")
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

    def get_epsilon_closure(self, states, transitions):
        """Compute the epsilon closure of a set of states for NFA."""
        closure = set(states)
        stack = list(states)
        while stack:
            state = stack.pop()
            if "epsilon" in transitions.get(state, {}):
                for next_state in transitions[state]["epsilon"]:
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
        return closure

    def trace_transitions(self, automaton, input_string, states, initial_state, final_states):
        """Trace the state transitions for an input string."""
        current_states = {initial_state}
        if isinstance(automaton, NFA):
            current_states = self.get_epsilon_closure(current_states, automaton.transitions)
        trace = [f"Start: {current_states}"]
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if isinstance(automaton, DFA):
                    if symbol in automaton.transitions.get(state, {}):
                        next_states.add(automaton.transitions[state][symbol])
                else:
                    if symbol in automaton.transitions.get(state, {}):
                        next_states.update(automaton.transitions[state][symbol])
            if isinstance(automaton, NFA):
                next_states = self.get_epsilon_closure(next_states, automaton.transitions)
            current_states = next_states
            trace.append(f"On '{symbol}': {current_states}")
        accepted = bool(current_states & final_states)
        trace.append(f"End: {current_states}, Accepted: {accepted}")
        return trace, accepted

    def test_input(self):
        try:
            states, alphabet, initial_state, final_states = self.parse_inputs()
            inputs = [s.strip() for s in self.input_string_entry.get().split(",") if s.strip()]
            if not inputs:
                raise ValueError("No input strings provided")
            if self.automaton_type.get() == "DFA":
                transitions = {state: {symbol: next(iter(dest)) for symbol, dest in trans.items()} for state, trans in self.transitions.items()}
                print("DFA Transitions:", transitions)  # Debug
                automaton = DFA(
                    states=states,
                    input_symbols=alphabet - {"epsilon"},
                    transitions=transitions,
                    initial_state=initial_state,
                    final_states=final_states
                )
            else:
                print("NFA Transitions:", self.transitions)  # Debug
                automaton = NFA(
                    states=states,
                    input_symbols=alphabet - {"epsilon"},
                    transitions=self.transitions,
                    initial_state=initial_state,
                    final_states=final_states
                )
            self.result_text.delete(1.0, tk.END)
            for inp in inputs:
                if any(c not in alphabet - {"epsilon"} for c in inp):
                    self.result_text.insert(tk.END, f"Input '{inp}' contains invalid symbols\n\n")
                    continue
                trace, accepted = self.trace_transitions(automaton, inp, states, initial_state, final_states)
                self.result_text.insert(tk.END, f"Trace for input '{inp}':\n" + "\n".join(trace) + "\n\n")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomatonVisualizerApp(root)
    root.mainloop()