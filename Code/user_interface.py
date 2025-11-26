import tkinter as tk
from tkinter import messagebox
from data_retrieval import DataRetrieval
from summarizer import Summarizer
from sentiment_analyzer import SentimentAnalyzer
from feedback_extractor import FeedbackExtractor
from PIL import Image, ImageTk
import threading
import re
import os
from datetime import datetime


def save_feedback_as_txt(what_works, needs_improvement, output_dir="reports"):
    os.makedirs(output_dir, exist_ok=True)
    filename = f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("YouTube Feedback Report\n")
        f.write("=======================\n\n")
        f.write("What’s Working:\n")
        f.write(what_works.strip() + "\n\n")
        f.write("Needs Improvement:\n")
        f.write(needs_improvement.strip() + "\n")

    print(f"Text report saved at: {filepath}")


class YouTubeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Video Analysis")
        self.geometry("960x700")
        self.configure(bg="#f8f9fa")

        self.frames = {}
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (HomePage, ResultsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

        self.video_summary = ""
        self.sentiment_data = {}
        self.feedback_data = {}

    def show_frame(self, page):
        self.frames[page].tkraise()

    def show_results_page(self):
        self.frames[ResultsPage].update_content(
            self.video_summary,
            self.sentiment_data,
            self.feedback_data
        )
        self.show_frame(ResultsPage)

    def load_video_data(self, video_url):
        youtube_api_key = os.getenv("YOUTUBE_API_KEY")
        gemini_api_key = os.getenv("GEMINI_API_KEY")

        dr = DataRetrieval(youtube_api_key, video_url)
        dr.validate_url()
        dr.get_metadata()
        transcript = dr.get_transcript()
        comments = dr.get_comments()

        self.video_summary = Summarizer(gemini_api_key).analyze(transcript)
        self.sentiment_data = SentimentAnalyzer().analyze(comments)

        feedback = FeedbackExtractor(gemini_api_key).analyze(comments)
        if feedback is None:
            feedback = {
                "what_works": "No feedback available.",
                "needs_improvement": "No improvement suggestions."
            }
        self.feedback_data = feedback

        save_feedback_as_txt(
            self.feedback_data["what_works"],
            self.feedback_data["needs_improvement"]
        )


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        try:
            bg_image = Image.open("assets/background.jpg").resize((960, 700))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(relwidth=1, relheight=1)
        except:
            pass

        content_frame = tk.Frame(self, bg="#ffffff", bd=2, highlightbackground="#cccccc", highlightthickness=1)
        content_frame.place(relx=0.5, rely=0.3, anchor="n")

        try:
            logo_img = Image.open("assets/youtube_logo.png").resize((100, 70))
            self.logo = ImageTk.PhotoImage(logo_img)
            tk.Label(content_frame, image=self.logo, bg="#ffffff").pack(pady=(10, 10))
        except:
            tk.Label(content_frame, text="🎬", font=("Helvetica", 36), bg="#ffffff").pack(pady=(10, 10))

        tk.Label(content_frame, text="YouTube Video Analyzer", font=("Helvetica", 24, "bold"),
                 bg="#ffffff", fg="#212529").pack(pady=(5, 25))

        entry_frame = tk.Frame(content_frame, bg="#ffffff")
        entry_frame.pack(pady=(0, 30), padx=20, fill="x")

        self.url_entry = tk.Entry(entry_frame, font=("Arial", 16), width=45, fg='gray', relief="solid", bd=1,
                                  highlightthickness=1, highlightcolor="#4285F4", highlightbackground="#dddddd")
        self.url_entry.insert(0, "Enter a YouTube video link...")
        self.url_entry.bind("<FocusIn>", self.clear_placeholder)
        self.url_entry.pack(side="left", ipady=8, padx=(0, 10), expand=True, fill="x")

        search_button = tk.Button(entry_frame, text="Analyze", font=("Arial", 13, "bold"),
                                  command=self.on_search, bg="#4285F4", fg="white", padx=20, pady=8, relief="flat",
                                  cursor="hand2")
        search_button.pack(side="left")

    def clear_placeholder(self, event):
        if self.url_entry.get() == "Enter a YouTube video link...":
            self.url_entry.delete(0, tk.END)
            self.url_entry.config(fg="black")

    def on_search(self):
        video_url = self.url_entry.get().strip()
        if not video_url or "youtube" not in video_url:
            messagebox.showerror("Error", "Please enter a valid YouTube video URL.")
            return

        self.loading_popup = tk.Toplevel(self)
        self.loading_popup.title("Analyzing")
        self.loading_popup.geometry("300x100")
        self.loading_popup.resizable(False, False)
        self.loading_popup.grab_set()

        self.status_label = tk.Label(self.loading_popup, text="Initializing...", font=("Arial", 12))
        self.status_label.pack(expand=True, pady=10)

        self.dots = 0
        self.animate_loading()
        threading.Thread(target=self.run_analysis, args=(video_url,), daemon=True).start()

    def animate_loading(self):
        if hasattr(self, 'loading_popup') and self.loading_popup.winfo_exists():
            self.dots = (self.dots + 1) % 4
            self.status_label.config(text=f"Analyzing video{'.' * self.dots}")
            self.after(500, self.animate_loading)

    def run_analysis(self, video_url):
        try:
            self.status_label.config(text="Fetching metadata...")
            self.controller.load_video_data(video_url)
            if hasattr(self, 'loading_popup'):
                self.loading_popup.destroy()
            self.controller.show_results_page()
        except Exception as e:
            if hasattr(self, 'loading_popup'):
                self.loading_popup.destroy()
            messagebox.showerror("Error", str(e))


class ResultsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        canvas = tk.Canvas(self, borderwidth=0, background="#f8f9fa")
        self.scroll_frame = tk.Frame(canvas, bg="#f8f9fa")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # === Background Image ===
        try:
            bg_image = Image.open("assets/background2.jpg").resize((960, 1600))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self.scroll_frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.scroll_frame.configure(bg="#e0e0e0")

        # === Header ===
        header = tk.Frame(self.scroll_frame, bg="#f8f9fa")
        header.pack(fill="x", padx=10, pady=(10, 5))

        tk.Button(header, text="← Return to Home", font=("Arial", 11, "bold"),
                  command=lambda: controller.show_frame(controller.frames.keys().__iter__().__next__()),
                  bg="#343a40", fg="white", padx=10, pady=5, relief="flat").pack(side="left")

        tk.Label(self.scroll_frame, text="📊 Video Analysis Results", font=("Helvetica", 18, "bold"),
                 bg="#f8f9fa").pack(pady=(5, 10))

        # === Summary Section ===
        self.summary_frame = self._create_section("📌 Video Summary")
        self.summary_text = self._create_text_label(self.summary_frame)

        # === Sentiment Section ===
        self.sentiment_frame = self._create_section("📈 Sentiment Analysis")
        self.sentiment_text = self._create_text_label(self.sentiment_frame)

        # === What's Working Section ===
        self.works_frame = self._create_section("✅ What’s Working")
        self.works_text = self._create_text_label(self.works_frame)

        # === Needs Improvement Section ===
        self.needs_frame = self._create_section("🛠 Needs Improvement")
        self.needs_text = self._create_text_label(self.needs_frame)

    def _create_section(self, title):
        frame = tk.Frame(self.scroll_frame, bg="#ffffff", bd=1, relief="solid")
        tk.Label(frame, text=title, font=("Helvetica", 16, "bold"), bg="#ffffff").pack(anchor="w", padx=10, pady=(5, 0))
        frame.pack(fill="x", padx=20, pady=10)
        return frame
    def _create_text_label(self, parent):
        label = tk.Label(parent, text="", wraplength=800, justify="left",
                         font=("Helvetica", 12), bg="#ffffff", anchor="w")
        label.pack(fill="x", padx=10, pady=(0, 10))
        return label
    def _remove_formatting(self, text):
        return re.sub(r'\*\*(.*?)\*\*', r'\1', text)

    def update_content(self, summary, sentiment, feedback):
        self.summary_text.config(text=self._remove_formatting(summary.strip()))

        total = sum(len(lst) for lst in sentiment.values()) or 1
        pos = (len(sentiment["positive"]) / total) * 100
        neg = (len(sentiment["negative"]) / total) * 100
        neu = (len(sentiment["neutral"]) / total) * 100
        sentiment_summary = f"Positive: {pos:.1f}%   Negative: {neg:.1f}%   Neutral: {neu:.1f}%"
        self.sentiment_text.config(text=sentiment_summary)

        self.works_text.config(text=self._remove_formatting(feedback.get("what_works", "").strip()))
        self.needs_text.config(text=self._remove_formatting(feedback.get("needs_improvement", "").strip()))

