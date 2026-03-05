import { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I can help you with country information. Ask me anything!",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [speakingMessageId, setSpeakingMessageId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Speech Recognition Setup
  const startListening = () => {
    if (
      !("webkitSpeechRecognition" in window) &&
      !("SpeechRecognition" in window)
    ) {
      alert(
        "Your browser does not support speech recognition. Please try Chrome or Edge.",
      );
      return;
    }

    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      console.error("Speech recognition error", event.error);
      setIsListening(false);
    };

    recognition.start();
  };

  const speakText = (text, messageId) => {
    if (!("speechSynthesis" in window)) {
      alert("Your browser does not support text-to-speech.");
      return;
    }

    // Cancel any current speech
    window.speechSynthesis.cancel();

    // Clean markdown for speech
    const cleanText = text
      .replace(/!\[.*?\]\(.*?\)/g, "") // Remove images
      .replace(/\|/g, ",") // Replace table pipes with commas
      .replace(/-/g, "") // Remove dashes
      .replace(/\*\*/g, "") // Remove bold
      .replace(/\*/g, "") // Remove italic
      .replace(/`/g, ""); // Remove code blocks

    const utterance = new SpeechSynthesisUtterance(cleanText);

    utterance.onstart = () => setSpeakingMessageId(messageId);
    utterance.onend = () => setSpeakingMessageId(null);
    utterance.onerror = () => setSpeakingMessageId(null);

    window.speechSynthesis.speak(utterance);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      let apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      // Render provides the host without protocol, so we add it if missing
      if (!apiUrl.startsWith("http")) {
        apiUrl = `https://${apiUrl}`;
      }

      const response = await axios.post(`${apiUrl}/chat`, {
        question: input,
      });

      const assistantMessage = {
        role: "assistant",
        content: response.data.answer,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Error fetching response:", error);
      const errorMessage = {
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="earth-bg" aria-hidden="true" />
      <div className="app-container">
        <header className="chat-header">
          <h1>Country Info AI Agent</h1>
        </header>

        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message-row ${msg.role}`}>
              <div className={`message ${msg.role}`}>
                <div className="message-content">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      img: (props) => (
                        <div className="image-container">
                          <img {...props} style={{ maxWidth: "100%" }} />
                        </div>
                      ),
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                </div>
              </div>
              {msg.role === "assistant" && (
                <button
                  className={`speak-button ${speakingMessageId === index ? "speaking" : ""}`}
                  onClick={() => speakText(msg.content, index)}
                  title="Read aloud"
                >
                  {speakingMessageId === index ? "🔊" : "🔈"}
                </button>
              )}
            </div>
          ))}
          {isLoading && (
            <div className="message-row assistant">
              <div className="message assistant">
                <div className="message-content">Thinking...</div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="chat-input-form">
          <button
            type="button"
            className={`mic-button ${isListening ? "listening" : ""}`}
            onClick={startListening}
            disabled={isLoading}
            title="Speak input"
          >
            {isListening ? "🛑" : "🎤"}
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              isListening ? "Listening..." : "Ask about a country..."
            }
            disabled={isLoading || isListening}
          />
          <button type="submit" disabled={isLoading || !input.trim()}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
