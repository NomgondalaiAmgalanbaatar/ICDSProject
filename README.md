# 🚀 Advanced AI-Powered Chat System

A feature-rich, modern chat application with AI integration, real-time messaging, and a beautiful dark-themed UI built with Python.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-darkblue.svg)
![OpenAI](https://img.shields.io/badge/AI-OpenAI-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [AI & Services](#ai--services)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Protocols & Communication](#protocols--communication)
- [Interesting Code Implementations](#interesting-code-implementations)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

---

## 🌟 Overview

This is a **full-stack chat application** that combines traditional socket programming with modern AI capabilities. It features a sleek dark-themed GUI, real-time multi-user communication, AI-powered features, and secure authentication.

---

## 🛠️ Tech Stack

### **Core Technologies**

| Technology             | Purpose               | Details                                |
| ---------------------- | --------------------- | -------------------------------------- |
| **Python 3.8+**        | Primary Language      | Core application logic                 |
| **Socket Programming** | Network Communication | TCP/IP for client-server architecture  |
| **Threading**          | Concurrency           | Multi-threaded message handling        |
| **CustomTkinter**      | Modern UI Framework   | Dark-themed, modern GUI components     |
| **Tkinter**            | Base GUI              | Standard Python GUI toolkit            |
| **SQLite3**            | Database              | User authentication & data persistence |
| **JSON**               | Data Format           | Message serialization & protocol       |
| **Pickle**             | Serialization         | Chat history & index persistence       |

### **External Libraries**

```python
customtkinter      # Modern UI components
openai            # GPT-3.5-turbo & DALL-E 3 integration
hume              # Emotion AI (sentiment analysis)
textblob          # Natural language processing
python-dotenv     # Environment variable management
emoji             # Emoji support & rendering
Pillow (PIL)      # Image processing & display
bcrypt            # Password hashing & security
requests          # HTTP requests for AI services
```

---

## 🤖 AI & Services

### **1. OpenAI Integration**

#### **GPT-3.5-turbo (Chat AI)**

- **Context-Aware Conversations**: AI maintains chat history (last 20 messages) for contextual responses
- **User-Specific Context**: AI knows who is asking questions
- **In-Chat Activation**: Use `@ai <query>` to trigger AI responses
- **Broadcast Responses**: AI responses are visible to all room participants

**Implementation Highlights:**

```python
# ai_utils.py - Context-aware AI chat
def get_chat_response(self, history, user_message, username=None):
    messages = [{"role": "system", "content": "You are a helpful chat assistant"}]
    # Add last 10 messages for context
    context_messages = history[-10:]
    # User-specific context
    messages.append({"role": "system", "content": f"User asking: {username}"})
```

#### **DALL-E 3 (Image Generation)**

- **Text-to-Image**: Generate images from text prompts
- **Automatic Fallback**: Falls back to DALL-E 2 if DALL-E 3 unavailable
- **Base64 Encoding**: Images converted to base64 for network transmission
- **Broadcast to Room**: Generated images visible to all participants
- **Command**: `/aipic <prompt>` or `/aipic: <prompt>`

**Features:**

- 1024x1024 resolution (DALL-E 3)
- Quality options: standard/HD
- Automatic download & encoding
- Error handling with user feedback

#### **AI-Powered Features**

- **📝 Summary**: Summarize recent chat history (last 2000 characters)
- **🔑 Keywords**: Extract 5 main keywords from conversation
- **😊 Sentiment Analysis**: Emotion detection using Hume AI (with OpenAI fallback)

### **2. Hume AI (Emotion AI)**

- Sentiment analysis and emotion detection
- Emoji-based emotion representation
- Fallback to OpenAI for sentiment when Hume unavailable

---

## ✨ Key Features

### **🔐 Authentication System**

- **SQLite Database**: Secure user storage
- **bcrypt Hashing**: Industry-standard password encryption
- **Dual Mode**: Login & Signup in single interface
- **Validation**: Username (3+ chars), Password (4+ chars)
- **Session Management**: Prevents duplicate logins

### **💬 Real-Time Messaging**

- **Multi-User Chat Rooms**: Dynamic group creation
- **Peer-to-Peer**: Direct user connections
- **Message Broadcasting**: Messages sent to all room participants
- **Timestamp Support**: Automatic message timestamping
- **Date Headers**: Automatic date separators in chat

### **🎨 Modern UI/UX**

#### **Dark Theme Design**

- CustomTkinter dark-blue theme
- Color-coded messages:
  - 🟢 **Green** (#4ADE80): Your messages
  - ⚪ **White** (#FFFFFF): Peer messages
  - 🟡 **Yellow** (#FACC15): System messages
  - 🔵 **Cyan** (#38BDF8): AI responses

#### **Advanced Input Features**

- **Command History**: Navigate with ↑/↓ arrow keys
- **Autocomplete**: Tab completion for commands & usernames
- **Live Hints**: Real-time command/user suggestions
- **Emoji Picker**:
  - 5 categories (Smileys, Space, Food, Animals, Hearts)
  - 400+ curated emojis
  - Tabbed interface
- **Image Sharing**:
  - Support for PNG, JPEG, GIF, BMP, WebP, TIFF, ICO
  - Automatic format conversion
  - Thumbnail generation (300x300)
  - Animated GIF support (first frame)

#### **Sidebar Features**

- **Quick Actions**: Time, Who, Poem shortcuts
- **AI Tools**: Summary & Keywords buttons
- **Online Users**: Real-time user list (updates every 10s)
- **User Profile**: Display current username

### **📚 Shakespeare Sonnets Integration**

- **154 Sonnets**: Complete collection indexed
- **Roman Numeral Indexing**: Efficient poem retrieval
- **Search Functionality**: Find sonnets by keywords
- **Command**: `/poem <number>` (e.g., `/poem 18`)

### **🔍 Advanced Search**

- **Full-Text Search**: Search your chat history
- **Word Indexing**: Efficient message retrieval
- **Per-User Indices**: Personalized search results
- **Persistent Storage**: Indices saved as `.idx` files

### **🎵 Audio Feedback**

- **Windows Sound**: Message send/receive notifications
- **Different Tones**:
  - Send: `MB_ICONASTERISK`
  - Receive: `MB_ICONEXCLAMATION`

### **📸 Image Handling**

- **Multiple Formats**: PNG, JPEG, GIF, BMP, WebP, TIFF, ICO
- **Smart Conversion**: Automatic format normalization
- **Transparency Handling**: RGBA → RGB with white background
- **Size Optimization**: 300x300 thumbnail, ~1.5MB limit
- **Base64 Transmission**: Efficient network transfer
- **In-Chat Display**: Images embedded in conversation

---

## 🏗️ Architecture

### **Client-Server Model**

```
┌─────────────┐         TCP/IP          ┌─────────────┐
│   Client    │ ←──────────────────────→ │   Server    │
│   (GUI.py)  │    JSON Messages        │ (server.py) │
└─────────────┘                          └─────────────┘
      │                                         │
      │                                         │
      ├─ CustomTkinter UI                      ├─ Socket Listener
      ├─ State Machine                         ├─ Group Manager
      ├─ AI Handler                            ├─ AI Handler
      └─ Message Processor                     ├─ Database
                                                ├─ Indexer
                                                └─ Chat History
```

### **State Machine**

```python
S_OFFLINE    → S_LOGGEDIN → S_CHATTING
   ↑              ↓              ↓
   └──────────────┴──────────────┘
```

### **Group Management**

- Dynamic chat room creation
- Multi-user support
- Automatic cleanup on disconnect
- State tracking (ALONE/TALKING)

---

## 🌐 Protocols & Communication

### **Message Protocol (JSON)**

All messages use JSON format for structured communication:

#### **Authentication**

```json
{
  "action": "login|signup",
  "name": "username",
  "password": "password"
}
```

#### **Chat Messages**

```json
{
  "action": "exchange",
  "from": "[username]",
  "message": "text",
  "time": "dd.mm.yy,HH:MM"
}
```

#### **Image Transfer**

```json
{
  "action": "image",
  "from": "username",
  "data": "base64_encoded_image"
}
```

#### **AI Queries**

```json
{
  "action": "ai_query",
  "query": "user question"
}
```

#### **AI Image Generation**

```json
{
  "action": "ai_image",
  "prompt": "image description"
}
```

#### **Commands**

```json
{
  "action": "time|who|list|poem|search|connect|disconnect",
  "target": "optional_parameter"
}
```

### **Network Layer**

- **Protocol**: TCP/IP
- **Port**: Configurable (default in SERVER constant)
- **Blocking**: Non-blocking sockets with `select()`
- **Encoding**: UTF-8 for text, Base64 for binary

### **Data Persistence**

| Data Type        | Storage Method | File Format      |
| ---------------- | -------------- | ---------------- |
| User Credentials | SQLite         | `users.db`       |
| Chat History     | Pickle         | `<username>.idx` |
| Message Indices  | Pickle         | `<username>.idx` |
| Sonnets Index    | Pickle         | `roman.txt.pk`   |

---

## 💡 Interesting Code Implementations

### **1. Context-Aware AI Chat**

```python
# Server maintains chat history per user (last 20 messages)
self.chat_history = {}  # {username: deque([msg1, msg2, ...], maxlen=20)}

# AI gets full context when responding
history = list(self.chat_history.get(from_name, []))
ai_response = self.ai.get_chat_response(history, query, from_name)
```

### **2. Smart Image Processing**

```python
# Handle all image formats with automatic conversion
if img.mode in ('RGBA', 'LA', 'P'):
    background = Image.new('RGB', img.size, (255, 255, 255))
    if img.mode == 'P':
        img = img.convert('RGBA')
    background.paste(img, mask=img.split()[-1])
    img = background
```

### **3. Autocomplete System**

```python
# Command autocomplete
if text.startswith("/") and " " not in text:
    matches = [c for c in self.commands if c.startswith(text)]

# User autocomplete for /connect
elif text.startswith("/connect "):
    partial = text.replace("/connect ", "")
    matches = [u for u in self.online_users if u.startswith(partial)]
```

### **4. Thread-Safe GUI Updates**

```python
def _display_system_message(self, text, tag=None):
    if threading.current_thread() is not threading.main_thread():
        # Schedule on main thread
        self.Window.after(0, lambda: self._display_system_message(text, tag))
        return
    # Safe to update GUI
    self.textCons.insert(END, text + "\n", tag)
```

### **5. Efficient Message Indexing**

```python
class Index:
    def add_msg_and_index(self, m):
        self.add_msg(m)
        line_at = self.total_msgs - 1
        words = m.split()
        for wd in words:
            if wd not in self.index:
                self.index[wd] = [line_at]
            else:
                self.index[wd].append(line_at)
```

### **6. Roman Numeral Poem Indexing**

```python
# Efficient sonnet retrieval using Roman numerals
def get_poem(self, p):
    p_str = self.int2roman[p] + '.'
    p_next_str = self.int2roman[p + 1] + '.'
    [(go_line, m)] = self.search(p_str)
    # Extract lines between Roman numerals
```

### **7. Dynamic Group Management**

```python
def connect(self, me, peer):
    peer_in_group, group_key = self.find_group(peer)
    if peer_in_group:
        # Join existing group
        self.chat_grps[group_key].append(me)
    else:
        # Create new group
        self.grp_ever += 1
        self.chat_grps[self.grp_ever] = [me, peer]
```

### **8. DALL-E 3 with Fallback**

```python
try:
    # Try DALL-E 3 first (better quality)
    response = self.openai_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard"
    )
except Exception as e:
    # Fallback to DALL-E 2
    response = self.openai_client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        size="512x512"
    )
```

---

## 📦 Installation

### **Prerequisites**

- Python 3.8 or higher
- pip package manager
- OpenAI API key (for AI features)
- Hume API key (optional, for emotion AI)

### **Setup**

1. **Clone the repository**

```bash
git clone <repository-url>
cd simple_gui
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment variables**

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
HUME_API_KEY=your_hume_api_key_here  # Optional
```

4. **Initialize database**

```bash
# Database will be created automatically on first run
# Located at: users.db
```

---

## 🚀 Usage

### **Quick Start (Windows)**

Use the PowerShell launcher script:

```powershell
.\start_chat_system.ps1
```

This will:

1. Start the server
2. Launch Client 1
3. Launch Client 2

### **Manual Start**

**Start Server:**

```bash
python chat_server.py
```

**Start Client(s):**

```bash
python chat_cmdl_client.py
```

### **Commands**

| Command           | Description             | Example                    |
| ----------------- | ----------------------- | -------------------------- |
| `/time`           | Get current server time | `/time`                    |
| `/who`            | List all online users   | `/who`                     |
| `/connect <user>` | Connect to a user       | `/connect Alice`           |
| `/poem <number>`  | Get Shakespeare sonnet  | `/poem 18`                 |
| `/search <term>`  | Search chat history     | `/search love`             |
| `/aipic <prompt>` | Generate AI image       | `/aipic sunset over ocean` |
| `/clear`          | Clear chat screen       | `/clear`                   |
| `/quit`           | Exit application        | `/quit`                    |
| `@ai <query>`     | Ask AI a question       | `@ai what is Python?`      |
| `bye`             | Disconnect from chat    | `bye`                      |

### **Keyboard Shortcuts**

- **↑/↓**: Navigate command history
- **Tab**: Autocomplete commands/usernames
- **Enter**: Send message
- **😊 Button**: Open emoji picker
- **📷 Button**: Send image

---

## 📁 Project Structure

```
simple_gui/
├── GUI.py                    # Main client GUI (884 lines)
├── chat_server.py            # Server implementation (308 lines)
├── chat_cmdl_client.py       # Client entry point
├── chat_client_class.py      # Client class wrapper
├── client_state_machine.py   # Client state management (161 lines)
├── chat_group.py             # Group/room management (124 lines)
├── chat_utils.py             # Shared utilities & constants
├── ai_utils.py               # AI integration (166 lines)
├── database.py               # SQLite authentication (139 lines)
├── indexer.py                # Message indexing (91 lines)
├── roman2num.py              # Roman numeral conversion
├── start_chat_system.ps1     # Windows launcher script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (not in repo)
├── users.db                  # SQLite database (auto-created)
├── AllSonnets.txt            # Shakespeare sonnets corpus
├── roman.txt.pk              # Roman numeral index (pickle)
└── *.idx                     # User chat indices (auto-created)
```

---

## 🎯 Features Breakdown

### **Authentication & Security**

- ✅ SQLite database with bcrypt hashing
- ✅ Signup/Login dual-mode interface
- ✅ Password validation (min 4 chars)
- ✅ Username validation (min 3 chars)
- ✅ Duplicate login prevention

### **Messaging**

- ✅ Real-time multi-user chat
- ✅ Group chat rooms
- ✅ Peer-to-peer connections
- ✅ Message broadcasting
- ✅ Timestamp support
- ✅ Date headers

### **AI Integration**

- ✅ GPT-3.5-turbo chat with context
- ✅ DALL-E 3 image generation
- ✅ Chat summarization
- ✅ Keyword extraction
- ✅ Sentiment analysis (Hume AI)
- ✅ User-specific AI context

### **UI/UX**

- ✅ Dark theme (CustomTkinter)
- ✅ Color-coded messages
- ✅ Emoji picker (400+ emojis)
- ✅ Image sharing
- ✅ Command autocomplete
- ✅ User autocomplete
- ✅ Command history (↑/↓)
- ✅ Live hints
- ✅ Audio feedback

### **Advanced Features**

- ✅ Full-text search
- ✅ Message indexing
- ✅ Shakespeare sonnets (154)
- ✅ Roman numeral indexing
- ✅ Persistent chat history
- ✅ Online user list
- ✅ Dynamic groups

---

## 🔧 Configuration

### **Server Configuration**

Edit `chat_utils.py`:

```python
SERVER = ('localhost', 50007)  # Change host/port
```

### **AI Configuration**

Edit `.env`:

```env
OPENAI_API_KEY=sk-...
HUME_API_KEY=...
```

### **UI Theme**

Edit `GUI.py`:

```python
ctk.set_appearance_mode("Dark")  # "Light", "Dark", "System"
ctk.set_default_color_theme("dark-blue")  # "blue", "green", "dark-blue"
```

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Voice chat integration
- File transfer support
- End-to-end encryption
- Mobile client
- Web interface
- More AI models (Claude, Gemini)
- Video chat
- Screen sharing

---

## 📄 License

This project is open-source and available under the MIT License.

---

## 👥 Authors

- **Original Authors**: alina, zzhang, bing
- **Refactored & Enhanced**: (Dec 2025)
  - Modern UI with CustomTkinter
  - AI Integration (OpenAI, Hume)
  - Advanced features (emoji, images, autocomplete)
  - SQLite authentication
  - Context-aware AI chat

---

## 🙏 Acknowledgments

- **OpenAI** for GPT-3.5-turbo and DALL-E 3 APIs
- **Hume AI** for emotion detection
- **CustomTkinter** for modern UI components
- **Shakespeare** for the sonnets corpus

---

## 📞 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Check existing documentation
- Review the code comments

---

**Built with ❤️ using Python, AI, and modern design principles**
