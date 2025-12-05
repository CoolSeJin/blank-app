# streamlit_app.py
import streamlit as st
import random
import time
import json
from pathlib import Path
import base64
from io import BytesIO

# 페이지 설정
st.set_page_config(
    page_title="🔦 방탈출 공포 게임 - Streamlit 버전",
    page_icon="👻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    /* 메인 헤더 */
    .main-header {
        font-size: 2.5rem;
        color: #ff4b4b;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* 게임 화면 */
    .game-screen {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        border: 3px solid #333;
        box-shadow: 0 10px 30px rgba(255,0,0,0.1);
        min-height: 500px;
        position: relative;
        overflow: hidden;
    }
    
    /* 방 이미지 */
    .room-image {
        width: 100%;
        border-radius: 10px;
        margin: 20px 0;
        border: 2px solid #444;
        transition: all 0.3s ease;
    }
    
    /* 선택 버튼 */
    .choice-button {
        background: linear-gradient(135deg, #2d2d44 0%, #1a1a2e 100%);
        border: 2px solid #444;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
    }
    
    .choice-button:hover {
        background: linear-gradient(135deg, #3d3d5a 0%, #2a2a3e 100%);
        border-color: #ff4b4b;
        transform: translateX(5px);
    }
    
    /* 인벤토리 */
    .inventory-item {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        padding: 8px 15px;
        margin: 5px;
        border-radius: 20px;
        border: 1px solid #444;
    }
    
    /* 상태 바 */
    .status-bar {
        display: flex;
        justify-content: space-between;
        background: rgba(0,0,0,0.7);
        padding: 10px 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    /* 점프스케어 */
    .jumpscare {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: black;
        z-index: 9999;
        animation: scare 2s ease-in-out;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    @keyframes scare {
        0% { background: black; }
        20% { background: red; }
        40% { background: black; }
        60% { background: red; }
        80% { background: black; }
        100% { background: transparent; }
    }
    
    .monster-text {
        color: white;
        font-size: 4rem;
        text-align: center;
        animation: pulse 0.5s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* 퍼즐 창 */
    .puzzle-window {
        background: rgba(0,0,0,0.9);
        border: 3px solid #ff4b4b;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }
    
    /* 메시지 */
    .game-message {
        background: rgba(255, 75, 75, 0.1);
        border-left: 5px solid #ff4b4b;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        animation: fadeIn 0.5s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* 푸터 */
    .footer {
        text-align: center;
        margin-top: 30px;
        color: #666;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# 게임 데이터
class GameData:
    def __init__(self):
        self.rooms = {
            "서재": {
                "name": "서재",
                "description": "더러운 서재입니다. 먼지 덮인 책상이 보입니다. 책상 위에는 다섯 권의 책이 놓여 있습니다.",
                "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80",
                "puzzle": {
                    "type": "color_sequence",
                    "question": "책들을 색상 순서대로 나열하세요 (빨강, 파랑, 초록, 노랑, 보라)",
                    "answer": ["red", "blue", "green", "yellow", "purple"],
                    "reward": "서재 열쇠",
                    "hint": "책상 위 메모를 확인해보세요"
                },
                "choices": [
                    {"text": "📚 책을 조사한다", "action": "investigate_books"},
                    {"text": "🪑 책상을 살펴본다", "action": "check_desk"},
                    {"text": "🚪 문을 연다", "action": "exit", "condition": "has_key"},
                    {"text": "💤 휴식한다", "action": "rest"}
                ]
            },
            "실험실": {
                "name": "실험실",
                "description": "이상한 기계와 시약병들이 놓인 실험실입니다. 공기가 차갑고 냄새가 납니다.",
                "image": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80",
                "puzzle": {
                    "type": "chemical",
                    "question": "시약병을 안전한 순서로 배치하세요 (빨강 → 파랑 → 초록)",
                    "answer": ["A", "B", "C"],
                    "reward": "실험 로그",
                    "hint": "벽에 붙어있는 안전 수칙을 보세요"
                },
                "choices": [
                    {"text": "🧪 시약병을 조사한다", "action": "investigate_chemicals"},
                    {"text": "⚙️ 기계를 작동시킨다", "action": "operate_machine"},
                    {"text": "🔙 뒤로 돌아간다", "action": "go_back"},
                    {"text": "📝 문서를 읽는다", "action": "read_documents"}
                ]
            },
            "지하 감옥": {
                "name": "지하 감옥",
                "description": "쇠사슬과 피자국이 있는 지하 감옥입니다. 공기가 무겁고 으스스합니다.",
                "image": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80",
                "puzzle": {
                    "type": "number_lock",
                    "question": "4자리 숫자 암호를 입력하세요 (힌트: 3120)",
                    "answer": "3120",
                    "reward": "감옥 열쇠",
                    "hint": "쇠사슬을 세어보세요"
                },
                "choices": [
                    {"text": "🔒 자물쇠를 조사한다", "action": "investigate_lock"},
                    {"text": "⛓️ 쇠사슬을 확인한다", "action": "check_chains"},
                    {"text": "🔙 뒤로 돌아간다", "action": "go_back"},
                    {"text": "💀 피자국을 조사한다", "action": "check_blood"}
                ]
            },
            "탈출구": {
                "name": "탈출구",
                "description": "마지막 방입니다. 탈출구가 보이지만 여러 개의 자물쇠로 잠겨 있습니다.",
                "image": "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80",
                "puzzle": {
                    "type": "final",
                    "question": "모든 열쇠를 사용하여 탈출구를 여세요",
                    "answer": ["서재 열쇠", "실험 로그", "감옥 열쇠"],
                    "reward": "자유",
                    "hint": "모든 방의 퍼즐을 해결해야 합니다"
                },
                "choices": [
                    {"text": "🚪 탈출구를 연다", "action": "escape", "condition": "all_keys"},
                    {"text": "🔙 뒤로 돌아간다", "action": "go_back"},
                    {"text": "📋 아이템을 확인한다", "action": "check_items"}
                ]
            }
        }
        
        # 게임 상태 초기화
        if 'current_room' not in st.session_state:
            st.session_state.current_room = "서재"
            st.session_state.inventory = []
            st.session_state.sanity = 100
            st.session_state.health = 100
            st.session_state.game_over = False
            st.session_state.game_won = False
            st.session_state.puzzles_solved = {
                "서재": False,
                "실험실": False,
                "지하 감옥": False,
                "탈출구": False
            }
            st.session_state.jumpscare_cooldown = 0
            st.session_state.messages = []
            st.session_state.show_puzzle = False
            st.session_state.puzzle_input = ""
            st.session_state.last_action_time = time.time()
            st.session_state.room_history = ["서재"]

# 게임 로직
class GameLogic:
    def __init__(self, game_data):
        self.data = game_data
    
    def add_message(self, text, type="info"):
        timestamp = time.strftime("%H:%M:%S")
        st.session_state.messages.insert(0, {
            "text": text,
            "type": type,
            "time": timestamp
        })
        if len(st.session_state.messages) > 10:
            st.session_state.messages = st.session_state.messages[:10]
    
    def trigger_jumpscare(self):
        if st.session_state.jumpscare_cooldown > 0:
            return
        
        st.session_state.jumpscare_active = True
        st.session_state.sanity = max(0, st.session_state.sanity - 20)
        st.session_state.jumpscare_cooldown = 5  # 5초 쿨다운
        
        # 2초 후 점프스케어 제거
        time.sleep(2)
        st.session_state.jumpscare_active = False
    
    def update_sanity(self):
        # 시간이 지날수록 정신력 감소
        current_time = time.time()
        time_passed = current_time - st.session_state.last_action_time
        
        if time_passed > 30:  # 30초 이상 아무것도 안하면
            st.session_state.sanity = max(0, st.session_state.sanity - 5)
            st.session_state.last_action_time = current_time
        
        # 정신력이 낮을수록 점프스케어 확률 증가
        if st.session_state.sanity < 50:
            if random.random() < 0.1:
                self.trigger_jumpscare()
    
    def handle_choice(self, choice):
        st.session_state.last_action_time = time.time()
        
        action = choice.get("action")
        condition = choice.get("condition")
        
        # 조건 체크
        if condition:
            if condition == "has_key" and "서재 열쇠" not in st.session_state.inventory:
                self.add_message("문이 잠겨 있습니다. 열쇠가 필요합니다.", "warning")
                return
            elif condition == "all_keys" and len(st.session_state.inventory) < 3:
                self.add_message("모든 열쇠가 필요합니다.", "warning")
                return
        
        # 액션 처리
        if action == "investigate_books":
            st.session_state.show_puzzle = True
            self.add_message("책들을 조사했습니다... 색상 순서가 중요할 것 같습니다.", "info")
        
        elif action == "check_desk":
            self.add_message("책상에서 낡은 메모지를 발견했습니다: '빨강, 파랑, 초록, 노랑, 보라'", "success")
            if random.random() < 0.2:
                self.trigger_jumpscare()
        
        elif action == "exit":
            st.session_state.room_history.append(st.session_state.current_room)
            if st.session_state.current_room == "서재":
                st.session_state.current_room = "실험실"
                self.add_message("실험실로 이동했습니다. 공기가 차갑습니다...", "info")
            elif st.session_state.current_room == "실험실":
                st.session_state.current_room = "지하 감옥"
                self.add_message("지하 감옥에 도착했습니다. 으스스한 기분이 듭니다.", "warning")
            elif st.session_state.current_room == "지하 감옥":
                st.session_state.current_room = "탈출구"
                self.add_message("탈출구가 보입니다! 하지만 여러 자물쇠가...", "info")
        
        elif action == "rest":
            st.session_state.sanity = min(100, st.session_state.sanity + 20)
            st.session_state.health = min(100, st.session_state.health + 10)
            self.add_message("휴식을 취했습니다. 정신력과 체력이 회복되었습니다.", "success")
        
        elif action == "investigate_lock":
            st.session_state.show_puzzle = True
            self.add_message("자물쇠를 조사했습니다... 4자리 숫자가 필요합니다.", "info")
        
        elif action == "check_chains":
            self.add_message("쇠사슬이 3개 있습니다. 이상하게도 숫자 '3'이 새겨져 있습니다.", "info")
            if random.random() < 0.3:
                self.trigger_jumpscare()
        
        elif action == "escape":
            if len(st.session_state.inventory) >= 3:
                st.session_state.game_won = True
                self.add_message("축하합니다! 탈출에 성공했습니다!", "success")
            else:
                self.add_message("아직 모든 열쇠를 모으지 못했습니다.", "warning")
        
        elif action == "go_back":
            if len(st.session_state.room_history) > 1:
                previous_room = st.session_state.room_history.pop()
                st.session_state.current_room = st.session_state.room_history[-1]
                self.add_message(f"{st.session_state.current_room}으로 돌아왔습니다.", "info")
        
        elif action == "operate_machine":
            self.add_message("기계가 웅웅거리기 시작합니다...", "warning")
            if random.random() < 0.4:
                self.trigger_jumpscare()
        
        # 점프스케어 쿨다운 감소
        if st.session_state.jumpscare_cooldown > 0:
            st.session_state.jumpscare_cooldown -= 1
    
    def solve_puzzle(self, puzzle_type, user_input):
        room = st.session_state.current_room
        puzzle = self.data.rooms[room]["puzzle"]
        
        if puzzle_type == "color_sequence":
            if user_input == puzzle["answer"]:
                st.session_state.puzzles_solved[room] = True
                st.session_state.inventory.append(puzzle["reward"])
                self.add_message(f"퍼즐 해결! {puzzle['reward']}을 얻었습니다!", "success")
                st.session_state.show_puzzle = False
                return True
        
        elif puzzle_type == "number_lock":
            if user_input == puzzle["answer"]:
                st.session_state.puzzles_solved[room] = True
                st.session_state.inventory.append(puzzle["reward"])
                self.add_message(f"자물쇠가 열렸습니다! {puzzle['reward']}을 얻었습니다!", "success")
                st.session_state.show_puzzle = False
                return True
        
        elif puzzle_type == "chemical":
            if user_input == puzzle["answer"]:
                st.session_state.puzzles_solved[room] = True
                st.session_state.inventory.append(puzzle["reward"])
                self.add_message(f"시약이 안정화되었습니다! {puzzle['reward']}을 얻었습니다!", "success")
                st.session_state.show_puzzle = False
                return True
        
        self.add_message("틀렸습니다. 다시 시도해보세요.", "error")
        st.session_state.sanity = max(0, st.session_state.sanity - 10)
        return False

# UI 컴포넌트
class GameUI:
    def __init__(self, game_data, game_logic):
        self.data = game_data
        self.logic = game_logic
    
    def render_status_bars(self):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-item">
                <div>🧠 정신력</div>
                <div class="stat-value">{st.session_state.sanity}%</div>
                <progress value="{st.session_state.sanity}" max="100"></progress>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-item">
                <div>❤️ 체력</div>
                <div class="stat-value">{st.session_state.health}%</div>
                <progress value="{st.session_state.health}" max="100"></progress>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            current_room = st.session_state.current_room
            st.markdown(f"""
            <div class="stat-item">
                <div>📍 현재 위치</div>
                <div class="stat-value">{current_room}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            solved_count = sum(st.session_state.puzzles_solved.values())
            st.markdown(f"""
            <div class="stat-item">
                <div>🎯 퍼즐 해결</div>
                <div class="stat-value">{solved_count}/4</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_inventory(self):
        if st.session_state.inventory:
            st.markdown("### 🎒 인벤토리")
            items_html = " ".join([f'<span class="inventory-item">{item}</span>' for item in st.session_state.inventory])
            st.markdown(f'<div>{items_html}</div>', unsafe_allow_html=True)
    
    def render_room(self):
        current_room = st.session_state.current_room
        room_data = self.data.rooms[current_room]
        
        st.markdown(f'<h2>{room_data["name"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p>{room_data["description"]}</p>', unsafe_allow_html=True)
        
        # 방 이미지
        st.image(room_data["image"], use_column_width=True)
        
        # 선택지
        st.markdown("### 무엇을 하시겠습니까?")
        
        for choice in room_data["choices"]:
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("선택", key=f"choice_{choice['text']}"):
                    self.logic.handle_choice(choice)
            with col2:
                st.markdown(f'<div class="choice-button">{choice["text"]}</div>', unsafe_allow_html=True)
    
    def render_puzzle(self):
        if not st.session_state.show_puzzle:
            return
        
        current_room = st.session_state.current_room
        puzzle = self.data.rooms[current_room]["puzzle"]
        
        st.markdown('<div class="puzzle-window">', unsafe_allow_html=True)
        st.markdown(f"### 🧩 {current_room} 퍼즐")
        st.markdown(f"**문제:** {puzzle['question']}")
        st.markdown(f"*힌트: {puzzle['hint']}*")
        
        if puzzle["type"] == "color_sequence":
            st.markdown("색상을 순서대로 선택하세요:")
            colors = ["빨강", "파랑", "초록", "노랑", "보라"]
            selected = []
            
            cols = st.columns(5)
            for i, color in enumerate(colors):
                with cols[i]:
                    if st.button(color, key=f"color_{i}"):
                        selected.append(color)
            
            if selected:
                st.write(f"선택한 순서: {', '.join(selected)}")
                if len(selected) == 5:
                    # 색상을 영어로 변환
                    color_map = {
                        "빨강": "red",
                        "파랑": "blue",
                        "초록": "green",
                        "노랑": "yellow",
                        "보라": "purple"
                    }
                    answer = [color_map[c] for c in selected]
                    self.logic.solve_puzzle("color_sequence", answer)
        
        elif puzzle["type"] == "number_lock":
            code = st.text_input("4자리 숫자 입력:", max_chars=4, key="code_input")
            if st.button("확인"):
                self.logic.solve_puzzle("number_lock", code)
        
        elif puzzle["type"] == "chemical":
            st.markdown("시약병 순서를 선택하세요:")
            cols = st.columns(3)
            with cols[0]:
                if st.button("A (빨강)", key="chem_a"):
                    self.logic.solve_puzzle("chemical", ["A"])
            with cols[1]:
                if st.button("B (파랑)", key="chem_b"):
                    self.logic.solve_puzzle("chemical", ["B"])
            with cols[2]:
                if st.button("C (초록)", key="chem_c"):
                    self.logic.solve_puzzle("chemical", ["C"])
        
        if st.button("퍼즐 닫기"):
            st.session_state.show_puzzle = False
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    def render_messages(self):
        if st.session_state.messages:
            st.markdown("### 📜 게임 로그")
            for msg in st.session_state.messages[:5]:
                if msg["type"] == "success":
                    icon = "✅"
                elif msg["type"] == "warning":
                    icon = "⚠️"
                elif msg["type"] == "error":
                    icon = "❌"
                else:
                    icon = "📝"
                
                st.markdown(f'<div class="game-message">{icon} [{msg["time"]}] {msg["text"]}</div>', unsafe_allow_html=True)
    
    def render_jumpscare(self):
        if hasattr(st.session_state, 'jumpscare_active') and st.session_state.jumpscare_active:
            monsters = ["👻", "💀", "👹", "🤡", "🧟", "🕷️", "🦇"]
            monster = random.choice(monsters)
            
            jumpscare_html = f"""
            <div class="jumpscare">
                <div class="monster-text">
                    {monster}<br>
                    <span style="font-size: 1.5rem;">무언가가 다가옵니다...</span>
                </div>
            </div>
            """
            st.markdown(jumpscare_html, unsafe_allow_html=True)
            st.rerun()

# 메인 앱
def main():
    st.markdown('<h1 class="main-header">🔦 방탈출 공포 게임</h1>', unsafe_allow_html=True)
    
    # 게임 초기화
    game_data = GameData()
    game_logic = GameLogic(game_data)
    game_ui = GameUI(game_data, game_logic)
    
    # 사이드바
    with st.sidebar:
        st.title("🎮 게임 컨트롤")
        st.markdown("---")
        
        # 게임 정보
        st.markdown("### 📊 게임 정보")
        game_ui.render_status_bars()
        
        st.markdown("---")
        
        # 인벤토리
        game_ui.render_inventory()
        
        st.markdown("---")
        
        # 설정
        st.markdown("### ⚙️ 설정")
        if st.button("🔄 게임 재시작"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        if st.button("💾 게임 저장"):
            st.success("게임 저장 기능은 준비 중입니다...")
        
        st.markdown("---")
        
        # 도움말
        with st.expander("❓ 게임 방법"):
            st.markdown("""
            ### 게임 목표
            모든 방의 퍼즐을 해결하고 탈출하세요!
            
            ### 조작법
            - 선택지 버튼을 클릭하여 행동
            - 퍼즐은 주의해서 해결
            - 정신력 관리가 중요
            
            ### 상태 표시
            - **정신력**: 낮을수록 공포 요소 증가
            - **체력**: 0이 되면 게임 오버
            - **인벤토리**: 획득한 아이템
            
            ### 팁
            - 너무 오래 같은 곳에 머무르지 마세요
            - 정기적으로 휴식하세요
            - 모든 단서를 주의깊게 살펴보세요
            """)
    
    # 메인 게임 영역
    game_container = st.container()
    
    with game_container:
        # 점프스케어 렌더링
        game_ui.render_jumpscare()
        
        # 게임 오버/승리 체크
        if st.session_state.game_won:
            st.balloons()
            st.success("🎉 축하합니다! 게임을 클리어하셨습니다!")
            st.markdown("""
            ### 게임 클리어!
            
            당신은 어둠 속에서 모든 퍼즐을 해결하고 탈출했습니다.
            
            **통계:**
            - 최종 정신력: {}%
            - 최종 체력: {}%
            - 소요 시간: {}초
            - 획득 아이템: {}
            """.format(
                st.session_state.sanity,
                st.session_state.health,
                int(time.time() - st.session_state.last_action_time),
                len(st.session_state.inventory)
            ))
            
            if st.button("🏠 메인 메뉴로 돌아가기"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            return
        
        if st.session_state.sanity <= 0 or st.session_state.health <= 0:
            st.error("💀 게임 오버!")
            st.markdown("""
            ### 실패 원인
            {}
            
            **최종 기록:**
            - 위치: {}
            - 인벤토리: {}
            - 해결한 퍼즐: {}/4
            """.format(
                "정신력이 모두 소진되었습니다." if st.session_state.sanity <= 0 else "체력이 모두 소진되었습니다.",
                st.session_state.current_room,
                ", ".join(st.session_state.inventory) if st.session_state.inventory else "없음",
                sum(st.session_state.puzzles_solved.values())
            ))
            
            if st.button("🔄 다시 시작하기"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            return
        
        # 게임 화면
        st.markdown('<div class="game-screen">', unsafe_allow_html=True)
        
        # 방 렌더링
        game_ui.render_room()
        
        # 퍼즐 렌더링
        game_ui.render_puzzle()
        
        # 메시지 렌더링
        game_ui.render_messages()
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 정신력 업데이트
        game_logic.update_sanity()
        
        # 자동 새로고침 (공포 효과를 위해)
        time.sleep(0.1)
        if random.random() < 0.05 and st.session_state.sanity < 50:
            st.rerun()
    
    # 푸터
    st.markdown("""
    <div class="footer">
    <hr>
    <p>© 2024 Streamlit 방탈출 게임 | 개발자: 게임 스튜디오</p>
    <p>이 게임은 순전히 Streamlit으로 제작되었습니다.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
