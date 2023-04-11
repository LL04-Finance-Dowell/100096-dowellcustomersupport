import { useState } from "react";
import "./App.css";
import Another from "./Another";

function App() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const handleMessageSend = () => {
    if (message.trim() === "") {
      return;
    }

    const newMessage = { text: message, sender: "" };
    const updatedMessages = [...messages, newMessage];
    setMessages(updatedMessages);

    // Clear the input field
    setMessage("");
  };
  return (
    <div className="App">
      <Another/>
      {/* <div>
        <>
          <button
            className="fixed bottom-20 right-10 bg-blue-400 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full h-14 w-14"
            onClick={() => setIsOpen(true)}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="currentColor"
              class="bi bi-chat-square-text h-6 w-6"
              viewBox="0 0 16 16"
            >
              {" "}
              <path d="M14 1a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-2.5a2 2 0 0 0-1.6.8L8 14.333 6.1 11.8a2 2 0 0 0-1.6-.8H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2.5a1 1 0 0 1 .8.4l1.9 2.533a1 1 0 0 0 1.6 0l1.9-2.533a1 1 0 0 1 .8-.4H14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z" />{" "}
              <path d="M3 3.5a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5zM3 6a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9A.5.5 0 0 1 3 6zm0 2.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5z" />{" "}
            </svg>
          </button>

          {isOpen && (
            <div className="inset-0 z-50 flex items-end justify-end px-20 mt-36">
              <div
                className="absolute inset-0"
                onClick={() => setIsOpen(false)}
              ></div>
              <div
                className="bg-gray-50 rounded-lg shadow-lg p-6 transform transition-all duration-500 w-80 h-96"
                style={{
                  opacity: isOpen ? 1 : 0,
                  transform: isOpen ? "translateY(0)" : "translateY(-100%)",
                }}
              >
                <div className="flex justify-end items-end">
                  <button
                    className="bg-red-600 text-white font-normal w-8 h-8 -mt-3 items-end rounded-full"
                    onClick={() => setIsOpen(false)}
                  >
                    X
                  </button>
                </div>
                <div className="chat-box">
                <h3 class=" font-semibold text-md text-center text-white mt-5 bg-black">
                    Room 001
                  </h3>
                  <div className="chat-messages">
                  
                    {messages.map((msg, idx) => (
                      <div key={idx}>
                        <p
                          className={
                            msg.sender === ""
                              ? "text-end font-bold"
                              : "font-bold"
                          }
                        >
                          {msg.text}
                        </p>
                        <small className="font-bold text-md">
                          {msg.sender}
                        </small>
                      </div>
                    ))}
                  </div>

                  
                  <form className="chat-form">
                    <div className="relative w-full">
                      <input
                        type="text"
                        id="voice-search"
                        className="bg-gray-300 border -mt-10 border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-60 p-2 -mx-2"
                        required
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                      />
                      <button
                        type="button"
                        className="absolute inset-y-0 right-0 pr-10 -mt-10"
                        onClick={handleMessageSend}
                      >
                        <img
                          className="w-6 h-6"
                          src="https://png.pngtree.com/png-vector/20190418/ourlarge/pngtree-vector-laugh-emoji-icon-png-image_956208.jpg"
                          alt=""
                        />
                      </button>
                    </div>
                    <button
                      type="submit"
                      className="flex items-center py-2 -mt-10 px-5 text-sm font-medium text-white bg-green-400"
                      onClick={handleMessageSend}
                    >
                      <img
                        className="w-5 h-5"
                        src="https://i.pinimg.com/originals/b4/32/51/b43251d2db9fd2f29d7baf13415e196f.png"
                        alt=""
                      />
                    </button>
                  </form>
                </div>
              </div>
            </div>
          )}
        </>
      </div> */}
    </div>
  );
}

export default App;
