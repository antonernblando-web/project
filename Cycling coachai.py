import tkinter as tk
from tkinter import messagebox, ttk


BACKGROUND = "#101820"
PANEL = "#182732"
PANEL_LIGHT = "#213744"
TEXT = "#f4f1e8"
MUTED = "#a9b9bc"
ACCENT = "#f5a623"
GREEN = "#75c69a"
RED = "#e68787"


ZONES = {
	"Zone 1": "Recovery — 50-60% FTP / very easy, barely-there pressure on the pedals.",
	"Zone 2": "Endurance — 60-75% FTP / conversational, all-day pace.",
	"Zone 3": "Tempo — 75-90% FTP / comfortably hard, controlled breathing.",
	"Zone 4": "Threshold — 90-105% FTP / hard but sustainable for the interval.",
	"Zone 5": "VO2 Max — 105%+ FTP / very hard, short efforts only.",
}

SESSION_LIBRARY = {
	"Base fitness": {
		"Monday": ("Rest", "Take a full rest day. A short walk and light mobility are optional.", "Zone 1"),
		"Tuesday": ("Endurance ride", "45 min at a conversational pace. Keep the effort smooth and relaxed.", "Zone 2"),
		"Wednesday": ("Cadence skills", "40 min easy with 6 x 1 min high-cadence spins, 2 min easy between.", "Zone 2"),
		"Thursday": ("Rest", "Rest day. Prioritize food, fluids, and an early night.", "Zone 1"),
		"Friday": ("Tempo introduction", "50 min including 3 x 6 min comfortably hard, with 4 min easy between.", "Zone 3"),
		"Saturday": ("Long easy ride", "75 min at an easy, steady pace. Finish feeling like you could continue.", "Zone 2"),
		"Sunday": ("Recovery spin", "30 min very easy, or take another rest day if fatigue is lingering.", "Zone 1"),
	},
	"Build endurance": {
		"Monday": ("Rest", "Full rest day. Gentle mobility only.", "Zone 1"),
		"Tuesday": ("Sweet spot", "60 min including 3 x 8 min strong and controlled, with 4 min easy between.", "Zone 3-4"),
		"Wednesday": ("Endurance ride", "60 min steady and conversational. Keep your breathing under control.", "Zone 2"),
		"Thursday": ("Climbing strength", "55 min including 5 x 3 min seated uphill or heavy-gear efforts, 3 min easy.", "Zone 4"),
		"Friday": ("Rest", "Rest and refuel. No need to make up missed training.", "Zone 1"),
		"Saturday": ("Long ride", "2 hours mostly easy. Add 20 min at a steady tempo if you feel fresh.", "Zone 2-3"),
		"Sunday": ("Recovery spin", "40 min very easy with relaxed legs and light pressure on the pedals.", "Zone 1"),
	},
	"Race preparation": {
		"Monday": ("Rest", "Complete rest. Visualize your target event and check your equipment.", "Zone 1"),
		"Tuesday": ("Intervals", "70 min including 5 x 4 min hard, 4 min easy between. Stay technically smooth.", "Zone 5"),
		"Wednesday": ("Endurance ride", "60 min easy. Keep the effort low enough to recover from Tuesday.", "Zone 2"),
		"Thursday": ("Race efforts", "65 min including 3 x 8 min at target race effort, 5 min easy between.", "Zone 4"),
		"Friday": ("Rest", "Rest, hydrate, and prepare nutrition for your next key ride.", "Zone 1"),
		"Saturday": ("Event simulation", "2 hours with 3 x 10 min at race effort inside a mostly easy ride.", "Zone 3-4"),
		"Sunday": ("Recovery spin", "35 min easy or full rest. Choose recovery over extra training.", "Zone 1"),
	},
}


def build_plan(goal, days_available):
	plan = []
	for day, session in SESSION_LIBRARY[goal].items():
		if day == "Monday" or len(plan) < days_available:
			plan.append((day, *session))
	while len(plan) < 7:
		day = list(SESSION_LIBRARY[goal])[len(plan)]
		session = SESSION_LIBRARY[goal][day]
		plan.append((day, *session))
	return plan


# --- Free-text feeling analysis -------------------------------------------------
# Instead of numeric sliders, the coach now reads what you typed about how you
# feel today and how your last ride felt, and looks for keyword cues.

PAIN_WORDS = ["pain", "hurts", "hurt", "injury", "injured", "sharp", "swollen", "twinge"]
SORENESS_WORDS = ["sore", "soreness", "stiff", "heavy legs", "dead legs", "wrecked",
                  "destroyed", "trashed", "achy", "aching"]
FATIGUE_WORDS = ["tired", "exhausted", "no sleep", "didn't sleep", "barely slept",
                  "poor sleep", "bad sleep", "insomnia", "drained", "sleepy", "fatigued"]
TIME_WORDS = ["no time", "short on time", "busy", "rushed", "only have", "quick",
              "not much time", "little time"]
POSITIVE_WORDS = ["great", "good", "strong", "fresh", "energetic", "amazing",
                   "ready", "excited", "pumped", "fantastic"]
STRUGGLE_RIDE_WORDS = ["struggled", "struggle", "tough ride", "hard ride", "awful",
                        "terrible", "bad ride", "rough ride", "slow", "sluggish"]
GREAT_RIDE_WORDS = ["great ride", "amazing ride", "flew", "strong ride", "fast",
                     "smooth ride", "felt great", "felt good", "nailed it"]


def recommend_zone(combined_text):
	"""Return 'Zone 2' or 'Zone 3' (or a rest call) based on how the text reads."""
	if any(word in combined_text for word in PAIN_WORDS):
		return "Rest — no zone today"
	if any(word in combined_text for word in SORENESS_WORDS) or any(word in combined_text for word in FATIGUE_WORDS):
		return "Zone 2"
	if any(word in combined_text for word in TIME_WORDS):
		return "Zone 2"
	if any(word in combined_text for word in STRUGGLE_RIDE_WORDS):
		return "Zone 2"
	if any(word in combined_text for word in GREAT_RIDE_WORDS) or any(word in combined_text for word in POSITIVE_WORDS):
		return "Zone 3"
	return "Zone 2"


def analyze_feelings(today_text, ride_text):
	today_text = (today_text or "").lower().strip()
	ride_text = (ride_text or "").lower().strip()
	combined = f"{today_text} {ride_text}"

	if not today_text and not ride_text:
		return ("Tell me how you're feeling today and how your last ride went, "
		        "and I'll tailor today's advice — including which zone to ride in.")

	zone = recommend_zone(combined)
	zone_note = "" if zone.startswith("Rest") else f" Stay in {zone} today."

	if any(word in combined for word in PAIN_WORDS):
		return ("That sounds like more than normal soreness. Skip training today, "
		        "rest, and if the pain is sharp, persistent, or changes how you move, "
		        "please check in with a medical professional before riding again.")

	if any(word in combined for word in SORENESS_WORDS) and any(word in combined for word in FATIGUE_WORDS):
		return ("Sore legs and low energy together are a clear signal to back off." + zone_note +
		        " Keep it easy for 20-30 minutes, or take a full rest day if it doesn't ease up.")

	if any(word in combined for word in SORENESS_WORDS):
		return ("Your legs sound like they need a break." + zone_note +
		        " Nothing above conversational pace — the harder work will keep.")

	if any(word in combined for word in FATIGUE_WORDS):
		return ("Sounds like you're running low on rest." + zone_note +
		        " Skip any hard intervals; consistency beats one extra hard day.")

	if any(word in combined for word in TIME_WORDS):
		return ("A short ride still counts." + zone_note +
		        " Ride easy for whatever time you have, and skip the harder efforts today.")

	if any(word in combined for word in STRUGGLE_RIDE_WORDS):
		return ("Rides like that happen to everyone — it doesn't erase your progress." + zone_note +
		        " Take today easier than planned; expect the next one to feel better.")

	if any(word in combined for word in GREAT_RIDE_WORDS) or any(word in combined for word in POSITIVE_WORDS):
		return ("Sounds like you're in a good place." + zone_note +
		        " You can push into Zone 3 today if the planned session calls for it — "
		        "just start with 10 easy minutes first.")

	return ("Thanks for checking in." + zone_note +
	        " Keep the first 15 minutes easy and dial back if your legs don't come around.")


class CyclingCoach:
	def __init__(self, root):
		self.root = root
		self.root.title("Pacecraft | AI Cycling Coach")
		self.root.configure(bg=BACKGROUND)
		self.root.minsize(960, 700)
		self.plan = []
		self.create_widgets()
		self.generate_plan()

	def create_widgets(self):
		self.root.columnconfigure(1, weight=1)
		self.root.rowconfigure(0, weight=1)

		sidebar = tk.Frame(self.root, bg=PANEL, width=270)
		sidebar.grid(row=0, column=0, sticky="nsew")
		sidebar.grid_propagate(False)
		tk.Label(sidebar, text="PACECRAFT", bg=PANEL, fg=ACCENT, font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=26, pady=(30, 4))
		tk.Label(sidebar, text="AI CYCLING COACH", bg=PANEL, fg=TEXT, font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=26)
		tk.Label(sidebar, text="A flexible week built around how you actually feel.", bg=PANEL, fg=MUTED, wraplength=210, justify="left", font=("Segoe UI", 10)).pack(anchor="w", padx=26, pady=(8, 28))

		self.goal = self.field(sidebar, "Training focus", ["Base fitness", "Build endurance", "Race preparation"])
		self.days = self.field(sidebar, "Ride days per week", ["3", "4", "5", "6"])
		tk.Button(sidebar, text="GENERATE WEEK", command=self.generate_plan, bg=ACCENT, fg=BACKGROUND, activebackground="#ffc45b", relief="flat", font=("Segoe UI", 10, "bold"), cursor="hand2").pack(fill="x", padx=26, pady=(22, 8), ipady=10)

		tk.Label(sidebar, text="ZONE GUIDE", bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=26, pady=(20, 6))
		for zone_name, zone_desc in ZONES.items():
			row = tk.Frame(sidebar, bg=PANEL)
			row.pack(fill="x", padx=26, pady=2)
			tk.Label(row, text=zone_name, bg=PANEL, fg=ACCENT, font=("Segoe UI", 8, "bold"), width=8, anchor="w").pack(side="left")
			tk.Label(row, text=zone_desc, bg=PANEL, fg=MUTED, font=("Segoe UI", 7), wraplength=150, justify="left", anchor="w").pack(side="left")

		tk.Label(sidebar, text="Training guidance is educational, not medical advice. Stop for sharp pain, dizziness, or unusual symptoms.", bg=PANEL, fg=MUTED, wraplength=210, justify="left", font=("Segoe UI", 8)).pack(side="bottom", anchor="w", padx=26, pady=24)

		main = tk.Frame(self.root, bg=BACKGROUND)
		main.grid(row=0, column=1, sticky="nsew", padx=30, pady=26)
		main.columnconfigure(0, weight=1)
		main.rowconfigure(3, weight=1)
		tk.Label(main, text="Your training cockpit", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 24, "bold")).grid(row=0, column=0, sticky="w")
		tk.Label(main, text="Build momentum without outriding your recovery.", bg=BACKGROUND, fg=MUTED, font=("Segoe UI", 11)).grid(row=1, column=0, sticky="w", pady=(2, 18))

		# --- Readiness check-in, now free-text ---
		readiness = tk.Frame(main, bg=PANEL_LIGHT, padx=18, pady=15)
		readiness.grid(row=2, column=0, sticky="ew", pady=(0, 18))
		readiness.columnconfigure(0, weight=1)
		readiness.columnconfigure(1, weight=1)
		tk.Label(readiness, text="TODAY'S CHECK-IN", bg=PANEL_LIGHT, fg=ACCENT, font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

		tk.Label(readiness, text="How do you feel today?", bg=PANEL_LIGHT, fg=MUTED, font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w")
		self.today_input = tk.Text(readiness, height=3, width=36, bg=BACKGROUND, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word", font=("Segoe UI", 10))
		self.today_input.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(4, 0))

		tk.Label(readiness, text="How did your last ride feel?", bg=PANEL_LIGHT, fg=MUTED, font=("Segoe UI", 9)).grid(row=1, column=1, sticky="w")
		self.ride_input = tk.Text(readiness, height=3, width=36, bg=BACKGROUND, fg=TEXT, insertbackground=TEXT, relief="flat", wrap="word", font=("Segoe UI", 10))
		self.ride_input.grid(row=2, column=1, sticky="ew", pady=(4, 0))

		tk.Button(readiness, text="ASK THE COACH", command=self.update_readiness, bg=GREEN, fg=BACKGROUND, activebackground="#9be0b9", relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2").grid(row=3, column=0, columnspan=2, sticky="w", pady=(12, 0), ipadx=14, ipady=8)

		self.readiness_text = tk.Label(readiness, text="Type how you feel and hit \"Ask the coach\" for tailored advice.", bg=PANEL_LIGHT, fg=TEXT, wraplength=760, justify="left", font=("Segoe UI", 10))
		self.readiness_text.grid(row=4, column=0, columnspan=2, sticky="w", pady=(14, 0))

		plan_frame = tk.Frame(main, bg=BACKGROUND)
		plan_frame.grid(row=3, column=0, sticky="nsew")
		plan_frame.columnconfigure(0, weight=1)
		plan_frame.rowconfigure(1, weight=1)
		tk.Label(plan_frame, text="7-day plan", bg=BACKGROUND, fg=TEXT, font=("Segoe UI", 16, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))
		self.plan_box = tk.Listbox(plan_frame, bg=PANEL, fg=TEXT, selectbackground=ACCENT, selectforeground=BACKGROUND, relief="flat", borderwidth=0, font=("Consolas", 11), activestyle="none", height=9)
		self.plan_box.grid(row=1, column=0, sticky="nsew")
		self.plan_box.bind("<<ListboxSelect>>", self.show_session)
		self.details = tk.Label(plan_frame, text="Select a session to see the details.", bg=BACKGROUND, fg=MUTED, anchor="w", justify="left", wraplength=700, font=("Segoe UI", 10))
		self.details.grid(row=2, column=0, sticky="ew", pady=(12, 0))

	def field(self, parent, label, values):
		tk.Label(parent, text=label.upper(), bg=PANEL, fg=MUTED, font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=26, pady=(0, 5))
		variable = tk.StringVar(value=values[0])
		ttk.Combobox(parent, textvariable=variable, values=values, state="readonly", font=("Segoe UI", 10)).pack(fill="x", padx=26, pady=(0, 16), ipady=4)
		return variable

	def generate_plan(self):
		self.plan = build_plan(self.goal.get(), int(self.days.get()))
		self.plan_box.delete(0, tk.END)
		for day, name, _details, intensity in self.plan:
			self.plan_box.insert(tk.END, f"{day:<10}  {name:<22}  {intensity}")
		self.plan_box.selection_set(0)
		self.show_session()

	def show_session(self, _event=None):
		selection = self.plan_box.curselection()
		if not selection:
			return
		day, name, details, intensity = self.plan[selection[0]]
		self.details.config(text=f"{day}  /  {name}\n{details}\nIntensity: {intensity}")

	def update_readiness(self):
		today_text = self.today_input.get("1.0", "end").strip()
		ride_text = self.ride_input.get("1.0", "end").strip()
		self.readiness_text.config(text=analyze_feelings(today_text, ride_text))


if __name__ == "__main__":
	app = tk.Tk()
	CyclingCoach(app)
	app.mainloop()