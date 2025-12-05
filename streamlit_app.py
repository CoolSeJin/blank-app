# streamlit_app.py
import streamlit as st
import random
import time
import json
from pathlib import Path
import base64
from io import BytesIO
import numpy as np

# 페이지 설정
st.set_page_config(
    page_title="👻 방탈출 공포 게임 - 공포 버전",
    page_icon="💀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 (공포 요소 강화)
st.markdown("""
<style>
    /* 메인 헤더 - 더 무섭게 */
    .main-header {
        font-size: 3rem;
        color: #ff0000;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000;
        font-family: 'Creepster', cursive;
        animation: headerGlow 2s infinite alternate;
    }
    
    @keyframes headerGlow {
        0% { text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000; }
        100% { text-shadow: 0 0 15px #ff0000, 0 0 30px #ff0000, 0 0 40px #ff3333; }
    }
    
    /* 게임 화면 - 어둡고 으스스하게 */
    .game-screen {
        background: linear-gradient(135deg, #000000 0%, #0a0a0a 100%);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
        border: 3px solid #660000;
        box-shadow: 0 10px 30px rgba(255,0,0,0.2);
        min-height: 500px;
        position: relative;
        overflow: hidden;
    }
    
    /* 전등 깜빡임 효과 */
    .flicker {
        animation: flicker 0.3s infinite alternate;
    }
    
    @keyframes flicker {
        0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
            opacity: 1;
        }
        20%, 24%, 55% {
            opacity: 0.3;
        }
    }
    
    /* 방 이미지에 어두운 오버레이 */
    .room-image-container {
        position: relative;
        width: 100%;
        border-radius: 10px;
        margin: 20px 0;
        overflow: hidden;
    }
    
    .room-image-darkness {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        z-index: 1;
        transition: all 0.5s ease;
    }
    
    /* 선택 버튼 - 더 무섭게 */
    .choice-button {
        background: linear-gradient(135deg, #1a0000 0%, #330000 100%);
        border: 2px solid #660000;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: #ff9999;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: left;
        font-family: 'Courier New', monospace;
        position: relative;
        overflow: hidden;
    }
    
    .choice-button:hover {
        background: linear-gradient(135deg, #330000 0%, #660000 100%);
        border-color: #ff0000;
        transform: translateX(5px);
        box-shadow: 0 0 15px rgba(255, 0, 0, 0.5);
    }
    
    .choice-button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 0, 0, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .choice-button:hover::before {
        left: 100%;
    }
    
    /* 위험한 선택지 스타일 */
    .dangerous-choice {
        background: linear-gradient(135deg, #330000 0%, #990000 100%) !important;
        border-color: #ff3333 !important;
        color: #ffcccc !important;
        animation: pulseDanger 2s infinite;
    }
    
    @keyframes pulseDanger {
        0%, 100% { box-shadow: 0 0 5px rgba(255, 0, 0, 0.5); }
        50% { box-shadow: 0 0 20px rgba(255, 0, 0, 0.8); }
    }
    
    /* 인벤토리 아이템에 피 효과 */
    .inventory-item {
        display: inline-block;
        background: rgba(255, 0, 0, 0.1);
        padding: 8px 15px;
        margin: 5px;
        border-radius: 20px;
        border: 1px solid #660000;
        position: relative;
        overflow: hidden;
    }
    
    .inventory-item::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255, 0, 0, 0.1), transparent);
        transform: translateX(-100%);
    }
    
    .inventory-item:hover::after {
        animation: slide 1s forwards;
    }
    
    @keyframes slide {
        to { transform: translateX(100%); }
    }
    
    /* 상태 바 - 혈액 효과 */
    .status-bar {
        display: flex;
        justify-content: space-between;
        background: rgba(102, 0, 0, 0.3);
        padding: 10px 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #660000;
        backdrop-filter: blur(5px);
    }
    
    .stat-item {
        text-align: center;
        position: relative;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ff6666;
    }
    
    progress {
        width: 100%;
        height: 10px;
        border-radius: 5px;
        border: 1px solid #330000;
    }
    
    progress::-webkit-progress-bar {
        background-color: #1a0000;
        border-radius: 5px;
    }
    
    progress::-webkit-progress-value {
        background-color: #ff0000;
        border-radius: 5px;
        box-shadow: 0 0 5px #ff0000;
    }
    
    /* 강화된 점프스케어 */
    .jumpscare-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: black;
        z-index: 9999;
        animation: scareSequence 3s ease-in-out forwards;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    
    @keyframes scareSequence {
        0% { background: black; }
        10% { background: #660000; }
        15% { background: black; }
        25% { background: #990000; transform: scale(1.1); }
        30% { background: black; transform: scale(1); }
        40% { background: #cc0000; }
        45% { background: black; }
        55% { background: #ff0000; }
        60% { background: black; }
        70% { opacity: 1; }
        100% { opacity: 0; display: none; }
    }
    
    .monster-face {
        font-size: 8rem;
        text-align: center;
        animation: monsterShake 0.1s infinite;
        filter: drop-shadow(0 0 10px red);
    }
    
    @keyframes monsterShake {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        25% { transform: translate(-5px, 5px) rotate(-1deg); }
        50% { transform: translate(5px, -5px) rotate(1deg); }
        75% { transform: translate(-5px, -5px) rotate(-1deg); }
    }
    
    .scary-text {
        color: white;
        font-size: 3rem;
        text-align: center;
        margin-top: 20px;
        animation: textPulse 0.5s infinite;
        font-family: 'Creepster', cursive;
    }
    
    @keyframes textPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    /* 그림자 효과 */
    .shadow-figure {
        position: absolute;
        background: rgba(0, 0, 0, 0.7);
        border-radius: 50%;
        animation: shadowMove 10s infinite linear;
        z-index: 2;
    }
    
    @keyframes shadowMove {
        0% { transform: translateX(-100px) translateY(100px); }
        50% { transform: translateX(100px) translateY(-100px); }
        100% { transform: translateX(-100px) translateY(100px); }
    }
    
    /* 웨이브 효과 */
    .wave-effect {
        position: absolute;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,0,0,0.1) 0%, transparent 70%);
        animation: wavePulse 3s infinite;
        z-index: 0;
    }
    
    @keyframes wavePulse {
        0% { transform: scale(0.5); opacity: 0; }
        50% { opacity: 0.5; }
        100% { transform: scale(1.5); opacity: 0; }
    }
    
    /* 퍼즐 창 - 더 어둡게 */
    .puzzle-window {
        background: rgba(10, 0, 0, 0.95);
        border: 3px solid #ff0000;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    /* 메시지 - 피처럼 */
    .game-message {
        background: rgba(255, 0, 0, 0.05);
        border-left: 5px solid #ff0000;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
        animation: fadeIn 0.5s;
        position: relative;
        overflow: hidden;
    }
    
    .game-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 0, 0, 0.1), transparent);
        transform: translateX(-100%);
    }
    
    .game-message:hover::before {
        animation: slide 1s forwards;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* 심장박동 효과 */
    .heartbeat {
        animation: heartbeat 1.5s infinite;
    }
    
    @keyframes heartbeat {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* 피가 흐르는 효과 */
    .blood-drip {
        position: fixed;
        width: 2px;
        height: 50px;
        background: linear-gradient(to bottom, transparent, #ff0000, transparent);
        animation: drip 3s infinite;
        z-index: 100;
    }
    
    @keyframes drip {
        0% { transform: translateY(-50px); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(100vh); opacity: 0; }
    }
</style>

<link href="https://fonts.googleapis.com/css2?family=Creepster&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# 게임 데이터 (공포 요소 강화)
class GameData:
    def __init__(self):
        self.rooms = {
            "서재": {
                "name": "피로 물든 서재",
                "description": "피가 흐른 듯한 책들과 부서진 가구들... 어둠 속에서 무언가가 숨 쉬는 소리가 들립니다.",
                "image": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80",
                "darkness_level": 0.3,  # 어두움 정도
                "flicker_chance": 0.1,  # 전등 깜빡임 확률
                "shadow_count": 1,  # 그림자 개수
                "puzzle": {
                    "type": "blood_sequence",
                    "question": "책들에 묻은 피의 색깔 순서를 맞추세요 (짙은 피 → 선지혈 → 어두운 핏자국)",
                    "answer": ["dark_red", "fresh_red", "dark_stain"],
                    "reward": "피로 적힌 일기장",
                    "hint": "서랍 속의 검은 촉지에 희미한 글씨가..."
                },
                "choices": [
                    {"text": "📚 피범벅 책을 조사한다", "action": "investigate_books", "danger": 0.3},
                    {"text": "🩸 피자국을 따라간다", "action": "follow_blood", "danger": 0.7},
                    {"text": "🗝️ 서랍을 연다", "action": "open_drawer", "danger": 0.5},
                    {"text": "💀 해골 옆에서 휴식한다", "action": "rest_with_skull", "danger": 0.8},
                    {"text": "🚪 문을 연다", "action": "exit", "condition": "has_key"}
                ]
            },
            "실험실": {
                "name": "기괴한 실험실",
                "description": "알 수 없는 액체들이 끓고, 기괴한 기계음이 울립니다. 벽면에는 이상한 기호들이 새겨져 있습니다.",
                "image": "https://images.unsplash.com/photo-1532094349884-543bc11b234d?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80",
                "darkness_level": 0.5,
                "flicker_chance": 0.3,
                "shadow_count": 2,
                "puzzle": {
                    "type": "chemical_reaction",
                    "question": "위험한 화학물질을 안전하게 혼합하세요. 순서가 생사를 결정합니다...",
                    "answer": ["green", "blue", "red"],
                    "reward": "실험자 사망 기록",
                    "hint": "바닥에 널부러진 메모지가 힌트를 주는 것 같습니다..."
                },
                "choices": [
                    {"text": "🧪 끓는 액체를 맛본다", "action": "taste_chemical", "danger": 0.9},
                    {"text": "⚙️ 기괴한 기계를 작동시킨다", "action": "operate_strange_machine", "danger": 0.6},
                    {"text": "🔬 현미경으로 이상한 조직을 관찰한다", "action": "observe_tissue", "danger": 0.4},
                    {"text": "💉 주사기를 집어든다", "action": "take_syringe", "danger": 0.7},
                    {"text": "🔙 뒤로 도망친다", "action": "escape_back"}
                ]
            },
            "지하 감옥": {
                "name": "고문 감옥",
                "description": "쇠사슬 소리와 신음소리가 울려퍼집니다. 어둠 속에서 누군가의 숨소리가 점점 가까워집니다...",
                "image": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80",
                "darkness_level": 0.7,
                "flicker_chance": 0.5,
                "shadow_count": 3,
                "puzzle": {
                    "type": "scream_lock",
                    "question": "고통의 비명이 남긴 메시지를 해독하세요... 4자리 숫자가 당신을 살릴 수 있습니다.",
                    "answer": "1313",
                    "reward": "포로의 유서",
                    "hint": "벽에 새겨진 흠집을 세어보세요... 그것들이 숫자를 의미합니다."
                },
                "choices": [
                    {"text": "⛓️ 피묻은 쇠사슬을 만져본다", "action": "touch_bloody_chains", "danger": 0.8},
                    {"text": "🔦 어둠 속 소리를 따라간다", "action": "follow_dark_sound", "danger": 0.9},
                    {"text": "💀 해골을 조사한다", "action": "investigate_skull", "danger": 0.5},
                    {"text": "🩸 피웅덩이에 손을 담근다", "action": "dip_hand_blood", "danger": 0.7},
                    {"text": "😱 비명을 지른다", "action": "scream", "danger": 0.4}
                ]
            },
            "최종 방": {
                "name": "악몽의 근원",
                "description": "모든 공포가 시작된 곳. 공기가 얼어붙고, 심장이 멈출 듯한 공포가 몰려옵니다.",
                "image": "https://images.unsplash.com/photo-1513584684374-8bab748fbf90?ixlib=rb-1.2.1&auto=format&fit=crop&w=1200&q=80",
                "darkness_level": 0.9,
                "flicker_chance": 0.8,
                "shadow_count": 5,
                "puzzle": {
                    "type": "final_confrontation",
                    "question": "모든 아이템을 사용해 악몽과 대결하세요. 선택이 당신의 운명을 결정합니다.",
                    "answer": ["sacrifice", "fight", "escape"],
                    "reward": "자유 또는 영원한 공포",
                    "hint": "과거의 선택들이 지금의 당신을 만들었습니다..."
                },
                "choices": [
                    {"text": "⚔️ 모든 힘을 다해 맞선다", "action": "final_fight", "danger": 0.95},
                    {"text": "🙏 무언가에게 기도한다", "action": "pray_to_darkness", "danger": 0.6},
                    {"text": "💎 보석을 바친다", "action": "sacrifice_jewel", "danger": 0.3},
                    {"text": "🩸 자신의 피로 봉인한다", "action": "seal_with_blood", "danger": 0.7},
                    {"text": "😵 의식을 잃는다", "action": "faint", "danger": 0.5}
                ]
            }
        }
        
        # 게임 상태 초기화
        if 'current_room' not in st.session_state:
            st.session_state.current_room = "서재"
            st.session_state.inventory = []
            st.session_state.sanity = 100
            st.session_state.health = 100
            st.session_state.fear = 0  # 새로운 공포 지수
            st.session_state.game_over = False
            st.session_state.game_won = False
            st.session_state.puzzles_solved = {
                "서재": False,
                "실험실": False,
                "지하 감옥": False,
                "최종 방": False
            }
            st.session_state.jumpscare_cooldown = 0
            st.session_state.messages = []
            st.session_state.show_puzzle = False
            st.session_state.puzzle_input = ""
            st.session_state.last_action_time = time.time()
            st.session_state.room_history = ["서재"]
            st.session_state.flicker_active = False
            st.session_state.flicker_end_time = 0
            st.session_state.blood_drips = []
            st.session_state.shadow_positions = []
            st.session_state.traumatic_memories = []  # 트라우마 기억
            st.session_state.last_scream_time = 0
            st.session_state.heartbeat_rate = 60  # 심박수

# 게임 로직 (공포 요소 강화)
class GameLogic:
    def __init__(self, game_data):
        self.data = game_data
    
    def add_message(self, text, type="info", fear_effect=0):
        timestamp = time.strftime("%H:%M:%S")
        
        # 공포 효과에 따라 메시지 색상 변경
        if fear_effect > 0.7:
            type = "horror"
            text = f"💀 {text}"
        elif fear_effect > 0.4:
            type = "warning"
            text = f"⚠️ {text}"
        elif type == "success":
            text = f"✅ {text}"
        
        st.session_state.messages.insert(0, {
            "text": text,
            "type": type,
            "time": timestamp,
            "fear": fear_effect
        })
        
        if len(st.session_state.messages) > 10:
            st.session_state.messages = st.session_state.messages[:10]
        
        # 공포 효과 적용
        if fear_effect > 0:
            st.session_state.fear = min(100, st.session_state.fear + fear_effect * 20)
    
    def trigger_jumpscare(self, intensity=1.0):
        if st.session_state.jumpscare_cooldown > 0:
            return
        
        # 강도에 따라 다른 점프스케어
        if intensity > 0.8:
            st.session_state.jumpscare_type = "extreme"
            sanity_loss = 40
        elif intensity > 0.5:
            st.session_state.jumpscare_type = "strong"
            sanity_loss = 25
        else:
            st.session_state.jumpscare_type = "normal"
            sanity_loss = 15
        
        st.session_state.jumpscare_active = True
        st.session_state.sanity = max(0, st.session_state.sanity - sanity_loss)
        st.session_state.fear = min(100, st.session_state.fear + 30)
        st.session_state.jumpscare_cooldown = 8  # 8초 쿨다운
        st.session_state.last_jumpscare_time = time.time()
        
        # 트라우마 기억 추가
        traumatic_events = [
            "깨어있는 악몽",
            "피투성이 그림자",
            "이상한 속삭임",
            "차가운 손길",
            "붉은 눈빛"
        ]
        if random.random() < 0.5:
            event = random.choice(traumatic_events)
            if event not in st.session_state.traumatic_memories:
                st.session_state.traumatic_memories.append(event)
        
        # 혈적 효과 추가
        for _ in range(random.randint(3, 7)):
            x = random.randint(0, 100)
            st.session_state.blood_drips.append({
                "x": x,
                "speed": random.uniform(1, 3),
                "opacity": random.uniform(0.5, 1)
            })
        
        # 3초 후 점프스케어 제거
        st.session_state.jumpscare_end_time = time.time() + 3
    
    def trigger_flicker(self, duration=2):
        st.session_state.flicker_active = True
        st.session_state.flicker_end_time = time.time() + duration
        st.session_state.fear = min(100, st.session_state.fear + 5)
    
    def update_fear_effects(self):
        current_time = time.time()
        
        # 점프스케어 종료 체크
        if hasattr(st.session_state, 'jumpscare_end_time') and current_time > st.session_state.jumpscare_end_time:
            st.session_state.jumpscare_active = False
        
        # 깜빡임 종료 체크
        if st.session_state.flicker_active and current_time > st.session_state.flicker_end_time:
            st.session_state.flicker_active = False
        
        # 랜덤 깜빡임
        room_data = self.data.rooms[st.session_state.current_room]
        if random.random() < room_data["flicker_chance"]:
            self.trigger_flicker(random.uniform(0.5, 2))
        
        # 공포에 따른 효과
        if st.session_state.fear > 80:
            # 극도의 공포 상태
            if random.random() < 0.05:
                self.add_message("심장이 터질 것 같습니다...", "horror", 0.3)
            st.session_state.heartbeat_rate = 120 + random.randint(-20, 20)
            
        elif st.session_state.fear > 50:
            # 중간 공포 상태
            st.session_state.heartbeat_rate = 90 + random.randint(-10, 10)
            if random.random() < 0.02:
                self.trigger_jumpscare(0.3)
        
        # 점프스케어 쿨다운 감소
        if st.session_state.jumpscare_cooldown > 0:
            st.session_state.jumpscare_cooldown -= 1
        
        # 혈적 제거
        st.session_state.blood_drips = [
            drip for drip in st.session_state.blood_drips
            if drip["opacity"] > 0.1
        ]
    
    def handle_dangerous_choice(self, danger_level):
        """위험한 선택지 처리"""
        current_time = time.time()
        
        # 위험 수준에 따른 다양한 결과
        if random.random() < danger_level:
            # 실패: 부정적인 결과
            outcomes = [
                ("심장이 멎을 것 같은 공포에 휩싸입니다...", 0.6, -20, -10),
                ("무언가가 당신을 붙잡았습니다!", 0.8, -30, -15),
                ("갑작스런 통증이 몰려옵니다...", 0.4, -15, -20),
                ("공포에 질려 비명을 지릅니다!", 0.5, -10, -5),
                ("어둠 속에서 무언가가 움직입니다...", 0.7, -25, -10)
            ]
            
            outcome = random.choice(outcomes)
            self.add_message(outcome[0], "horror", outcome[1])
            st.session_state.sanity = max(0, st.session_state.sanity + outcome[2])
            st.session_state.health = max(0, st.session_state.health + outcome[3])
            
            if outcome[1] > 0.5:
                self.trigger_jumpscare(outcome[1])
            
            return False
        
        else:
            # 성공: 긍정적인 결과 (하지만 여전히 무섭다)
            successes = [
                ("위험을 피했지만, 무언가가 당신을 주시하고 있습니다...", 0.3, 5, 0),
                ("살아남았지만, 기억에 또 하나의 상처가...", 0.4, 0, 5),
                ("용감한 선택이었지만, 손이 떨립니다...", 0.2, 10, 0),
            ]
            
            success = random.choice(successes)
            self.add_message(success[0], "warning", success[1])
            st.session_state.sanity = min(100, st.session_state.sanity + success[2])
            st.session_state.health = min(100, st.session_state.health + success[3])
            
            return True
    
    def handle_choice(self, choice):
        st.session_state.last_action_time = time.time()
        
        action = choice.get("action")
        danger = choice.get("danger", 0)
        
        # 위험한 선택지 처리
        if danger > 0 and action not in ["exit", "go_back"]:
            if not self.handle_dangerous_choice(danger):
                return  # 실패했으면 더 이상 진행하지 않음
        
        # 액션 처리
        if action == "investigate_books":
            st.session_state.show_puzzle = True
            self.add_message("피로 얼룩진 책들을 펼쳤습니다... 글씨가 흐릿합니다.", "info", 0.2)
            if random.random() < 0.3:
                self.trigger_flicker()
        
        elif action == "follow_blood":
            self.add_message("피자국을 따라갔습니다... 소리가 점점 커집니다.", "warning", 0.5)
            st.session_state.fear = min(100, st.session_state.fear + 20)
            if random.random() < 0.6:
                self.trigger_jumpscare(0.7)
        
        elif action == "open_drawer":
            found_item = random.choice(["낡은 열쇠", "피 묻은 편지", "부서진 안경"])
            self.add_message(f"서랍에서 {found_item}을 발견했습니다!", "success", 0.1)
            if found_item == "낡은 열쇠":
                st.session_state.inventory.append(found_item)
        
        elif action == "rest_with_skull":
            rest_amount = random.randint(10, 30)
            fear_increase = random.randint(10, 25)
            st.session_state.sanity = min(100, st.session_state.sanity + rest_amount)
            st.session_state.fear = min(100, st.session_state.fear + fear_increase)
            self.add_message(f"해골 옆에서 휴식을 취했습니다... 정신력 +{rest_amount}, 공포 +{fear_increase}", "info", 0.4)
            
        elif action == "taste_chemical":
            effects = [
                ("입안에서 이상한 맛이 납니다... 시야가 흐려집니다.", -20, -10),
                ("갑작스런 통증! 무언가 잘못됐습니다!", -30, -20),
                ("기분이 이상해집니다... 환각이 시작되는 것 같습니다.", -40, 0)
            ]
            effect = random.choice(effects)
            self.add_message(effect[0], "horror", 0.8)
            st.session_state.sanity = max(0, st.session_state.sanity + effect[1])
            st.session_state.health = max(0, st.session_state.health + effect[2])
            self.trigger_jumpscare(0.9)
            
        elif action == "scream":
            current_time = time.time()
            if current_time - st.session_state.last_scream_time > 10:
                self.add_message("비명이 감옥을 울렸습니다... 어둠이 움직입니다!", "warning", 0.6)
                st.session_state.last_scream_time = current_time
                if random.random() < 0.8:
                    self.trigger_jumpscare(0.5)
            else:
                self.add_message("목이 잠긴 것 같습니다... 소리가 나지 않습니다.", "warning", 0.3)
        
        elif action == "touch_bloody_chains":
            visions = [
                "갑작스런 기억이 떠오릅니다... 고통스런 비명소리...",
                "쇠사슬이 아직 따뜻합니다... 누군가 방금까지 여기에 있었습니다.",
                "손에 피가 묻었습니다... 씻을 수 없을 것 같습니다."
            ]
            self.add_message(random.choice(visions), "horror", 0.7)
            st.session_state.sanity = max(0, st.session_state.sanity - 15)
            
        elif action == "exit":
            st.session_state.room_history.append(st.session_state.current_room)
            if st.session_state.current_room == "서재":
                st.session_state.current_room = "실험실"
                self.add_message("기괴한 소리가 들리는 실험실로 들어갑니다...", "warning", 0.4)
            elif st.session_state.current_room == "실험실":
                st.session_state.current_room = "지하 감옥"
                self.add_message("찬 바람이 부는 지하 감옥에 도착했습니다...", "horror", 0.6)
            elif st.session_state.current_room == "지하 감옥":
                st.session_state.current_room = "최종 방"
                self.add_message("모든 공포의 근원에 도달했습니다...", "horror", 0.8)
                
        elif action == "final_fight":
            if len(st.session_state.inventory) >= 3:
                win_chance = st.session_state.sanity / 100
                if random.random() < win_chance:
                    st.session_state.game_won = True
                    self.add_message("악몽을 물리쳤습니다! 하지만 승리의 대가는...", "success", 0.5)
                else:
                    self.add_message("패배했습니다... 영원한 어둠이 당신을 삼킵니다.", "horror", 1.0)
                    st.session_state.game_over = True
            else:
                self.add_message("충분한 힘이 없습니다...", "warning", 0.3)
        
        elif action == "go_back" or action == "escape_back":
            if len(st.session_state.room_history) > 1:
                previous_room = st.session_state.room_history.pop()
                st.session_state.current_room = st.session_state.room_history[-1]
                self.add_message(f"공포에 질려 {st.session_state.current_room}으로 도망쳤습니다...", "warning", 0.4)
                st.session_state.fear = min(100, st.session_state.fear + 10)
        
        # 선택 후 무작위 공포 이벤트
        if random.random() < 0.2:
            self.random_horror_event()
    
    def random_horror_event(self):
        """무작위 공포 이벤트 발생"""
        events = [
            lambda: self.add_message("등 뒤에서 숨소리가 들립니다...", "horror", 0.3),
            lambda: self.add_message("갑자기 추워집니다...", "warning", 0.2),
            lambda: self.trigger_flicker(1),
            lambda: self.add_message("벽 속에서 긁는 소리가 납니다...", "horror", 0.4),
            lambda: (self.add_message("무언가가 당신의 이름을 부릅니다...", "horror", 0.5) 
                    if random.random() < 0.5 else None),
            lambda: (self.add_message("피냄새가 강해집니다...", "warning", 0.3) 
                    if st.session_state.fear > 50 else None)
        ]
        
        event = random.choice(events)
        event()
    
    def solve_puzzle(self, puzzle_type, user_input):
        room = st.session_state.current_room
        puzzle = self.data.rooms[room]["puzzle"]
        
        success = False
        
        if puzzle_type == "blood_sequence":
            if user_input == puzzle["answer"]:
                success = True
        
        elif puzzle_type == "number_lock" or puzzle_type == "scream_lock":
            if user_input == puzzle["answer"]:
                success = True
        
        elif puzzle_type == "chemical_reaction":
            if user_input == puzzle["answer"]:
                success = True
        
        if success:
            st.session_state.puzzles_solved[room] = True
            st.session_state.inventory.append(puzzle["reward"])
            fear_effect = 0.2 if room != "최종 방" else 0.5
            self.add_message(f"퍼즐 해결! {puzzle['reward']}을 얻었습니다!", "success", fear_effect)
            st.session_state.show_puzzle = False
            
            # 퍼즐 해결 후 특수 이벤트
            if room == "지하 감옥":
                self.add_message("자물쇠가 열리는 소리와 함께... 비명이 멀리서 들려옵니다.", "horror", 0.4)
                self.trigger_flicker(3)
            
            return True
        else:
            self.add_message("틀렸습니다... 실수가 치명적일 수 있습니다.", "error", 0.3)
            st.session_state.sanity = max(0, st.session_state.sanity - 15)
            st.session_state.fear = min(100, st.session_state.fear + 10)
            
            # 실패시 추가 공포
            if random.random() < 0.5:
                self.random_horror_event()
            
            return False

# UI 컴포넌트 (공포 버전)
class GameUI:
    def __init__(self, game_data, game_logic):
        self.data = game_data
        self.logic = game_logic
    
    def render_status_bars(self):
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            sanity_color = "#ff6666" if st.session_state.sanity > 50 else "#ff0000"
            st.markdown(f"""
            <div class="stat-item">
                <div>🧠 정신력</div>
                <div class="stat-value" style="color: {sanity_color}">{st.session_state.sanity}%</div>
                <progress value="{st.session_state.sanity}" max="100"></progress>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            health_color = "#ff6666" if st.session_state.health > 50 else "#ff0000"
            st.markdown(f"""
            <div class="stat-item">
                <div>❤️ 체력</div>
                <div class="stat-value" style="color: {health_color}">{st.session_state.health}%</div>
                <progress value="{st.session_state.health}" max="100"></progress>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            fear_level = st.session_state.fear
            fear_text = "안정" if fear_level < 30 else "불안" if fear_level < 60 else "공포" if fear_level < 80 else "공황"
            fear_color = "#999999" if fear_level < 30 else "#ff9900" if fear_level < 60 else "#ff3300" if fear_level < 80 else "#ff0000"
            st.markdown(f"""
            <div class="stat-item">
                <div>😨 공포 지수</div>
                <div class="stat-value" style="color: {fear_color}">{fear_text}</div>
                <progress value="{fear_level}" max="100"></progress>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            current_room = st.session_state.current_room
            room_data = self.data.rooms[current_room]
            darkness = int(room_data["darkness_level"] * 100)
            st.markdown(f"""
            <div class="stat-item">
                <div>🌑 어둠 정도</div>
                <div class="stat-value">{darkness}%</div>
                <progress value="{darkness}" max="100"></progress>
            </div>
            """, unsafe_allow_html=True)
        
        with col5:
            heartbeat = st.session_state.heartbeat_rate
            st.markdown(f"""
            <div class="stat-item">
                <div>💓 심박수</div>
                <div class="stat-value" style="color: #ff6666">{heartbeat} BPM</div>
                <div style="font-size: 0.8rem; color: #ff9999">{"빠름" if heartbeat > 100 else "정상" if heartbeat > 60 else "느림"}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_inventory(self):
        if st.session_state.inventory:
            st.markdown("### 🎒 획득한 공포의 증거")
            items_html = " ".join([f'<span class="inventory-item">{item}</span>' for item in st.session_state.inventory])
            st.markdown(f'<div>{items_html}</div>', unsafe_allow_html=True)
    
    def render_room(self):
        current_room = st.session_state.current_room
        room_data = self.data.rooms[current_room]
        
        # 방 제목과 설명
        st.markdown(f'<h2 class="heartbeat">{room_data["name"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<p>{room_data["description"]}</p>', unsafe_allow_html=True)
        
        # 방 이미지 (어두움 효과 적용)
        darkness = room_data["darkness_level"]
        image_html = f"""
        <div class="room-image-container">
            <img src="{room_data['image']}" style="width: 100%; border-radius: 10px; filter: brightness({1 - darkness});">
            <div class="room-image-darkness" style="opacity: {darkness};"></div>
        </div>
        """
        st.markdown(image_html, unsafe_allow_html=True)
        
        # 그림자 효과
        if room_data["shadow_count"] > 0 and st.session_state.fear > 30:
            for i in range(room_data["shadow_count"]):
                size = random.randint(50, 150)
                left = random.randint(10, 90)
                top = random.randint(10, 90)
                shadow_html = f"""
                <div class="shadow-figure" style="
                    width: {size}px;
                    height: {size}px;
                    left: {left}%;
                    top: {top}%;
                    opacity: {0.1 + (st.session_state.fear / 200)};
                "></div>
                """
                st.markdown(shadow_html, unsafe_allow_html=True)
        
        # 선택지
        st.markdown("### ⚠️ 무엇을 하시겠습니까? (위험: 😨)")
        
        for choice in room_data["choices"]:
            danger = choice.get("danger", 0)
            danger_text = " " + "😨" * int(danger * 3 + 0.5) if danger > 0 else ""
            
            # 위험도에 따른 버튼 클래스
            button_class = "choice-button"
            if danger > 0.7:
                button_class += " dangerous-choice"
            
            col1, col2 = st.columns([1, 5])
            with col1:
                button_text = "선택" + ("⚠️" if danger > 0.5 else "")
                if st.button(button_text, key=f"choice_{choice['text']}_{random.randint(0, 1000)}"):
                    self.logic.handle_choice(choice)
                    st.rerun()
            with col2:
                st.markdown(f'<div class="{button_class}">{choice["text"]}{danger_text}</div>', unsafe_allow_html=True)
    
    def render_jumpscare(self):
        if hasattr(st.session_state, 'jumpscare_active') and st.session_state.jumpscare_active:
            # 다양한 점프스케어 종류
            if hasattr(st.session_state, 'jumpscare_type'):
                if st.session_state.jumpscare_type == "extreme":
                    monster = random.choice(["👹", "🧟", "🤡"])
                    text = random.choice(["죽어라!", "여기 있어...", "영원히 괴롭힐 것이다!"])
                elif st.session_state.jumpscare_type == "strong":
                    monster = random.choice(["👻", "💀", "🕷️"])
                    text = random.choice(["도망칠 곳은 없다", "뒤를 봐...", "여기까지야"])
                else:
                    monster = random.choice(["👽", "🎃", "🐍"])
                    text = random.choice(["깜짝이야!", "놀랐지?", "무섭지?"])
            else:
                monster = "👻"
                text = "무언가 다가온다..."
            
            jumpscare_html = f"""
            <div class="jumpscare-overlay">
                <div class="monster-face">{monster}</div>
                <div class="scary-text">{text}</div>
                <div style="color: #ff9999; margin-top: 20px; font-size: 1.2rem;">
                    정신력이 {st.session_state.sanity}% 남았습니다...
                </div>
            </div>
            """
            st.markdown(jumpscare_html, unsafe_allow_html=True)
            
            # 혈적 효과
            for drip in st.session_state.blood_drips:
                st.markdown(f"""
                <div class="blood-drip" style="
                    left: {drip['x']}%;
                    animation-duration: {drip['speed']}s;
                    opacity: {drip['opacity']};
                "></div>
                """, unsafe_allow_html=True)
    
    def render_flicker_effect(self):
        if st.session_state.flicker_active:
            flicker_html = """
            <style>
                .game-screen {
                    animation: flicker 0.3s infinite alternate;
                }
            </style>
            """
            st.markdown(flicker_html, unsafe_allow_html=True)
    
    def render_traumatic_memories(self):
        if st.session_state.traumatic_memories:
            with st.expander("💭 트라우마 기억 (마우스를 올리면...)", expanded=False):
                for memory in st.session_state.traumatic_memories:
                    st.markdown(f"• {memory}")
    
    def render_heartbeat_effect(self):
        heartbeat = st.session_state.heartbeat_rate
        if heartbeat > 100:
            heartbeat_html = """
            <style>
                @keyframes fastHeartbeat {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.02); }
                }
                .game-screen {
                    animation: fastHeartbeat 0.6s infinite;
                }
            </style>
            """
            st.markdown(heartbeat_html, unsafe_allow_html=True)

# 메인 앱
def main():
    st.markdown('<h1 class="main-header">👻 방탈출 공포 게임 - 공포 버전</h1>', unsafe_allow_html=True)
    
    # 경고 메시지
    with st.expander("⚠️ 경고: 이 게임은 매우 무섭습니다", expanded=True):
        st.warning("""
        ## ⚠️ 주의사항
        - 이 게임은 **강렬한 공포 요소**를 포함하고 있습니다
        - 심장이 약하신 분, 정신적 충격을 받기 쉬운 분은 플레이를 권장하지 않습니다
        - 갑작스런 점프스케어, 어두운 배경, 으스스한 소리 효과(상상)가 있습니다
        - 게임 중 불편함을 느끼면 즉시 중단해 주세요
        
        ### 게임 특징:
        - 선택지마다 **위험도**가 표시됩니다 (😨 많을수록 위험)
        - **정신력**이 낮아질수록 더 무서운 일들이 일어납니다
        - **공포 지수**가 높아질수록 환경이 변화합니다
        - 무작위 **점프스케어**와 **전등 깜빡임** 효과가 있습니다
        """)
        
        if st.checkbox("위 내용을 이해하고 게임을 시작합니다"):
            game_started = True
        else:
            st.stop()
    
    # 게임 초기화
    game_data = GameData()
    game_logic = GameLogic(game_data)
    game_ui = GameUI(game_data, game_logic)
    
    # 사이드바
    with st.sidebar:
        st.title("🎮 공포 컨트롤러")
        st.markdown("---")
        
        # 게임 정보
        st.markdown("### 📊 공포 상태")
        game_ui.render_status_bars()
        
        st.markdown("---")
        
        # 인벤토리
        game_ui.render_inventory()
        
        st.markdown("---")
        
        # 트라우마 기억
        game_ui.render_traumatic_memories()
        
        st.markdown("---")
        
        # 설정
        st.markdown("### ⚙️ 공포 설정")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 공포 재시작"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🌙 어둠 조절"):
                st.session_state.fear = min(100, st.session_state.fear + 10)
                st.rerun()
        
        if st.button("💀 지금 무서워요!"):
            game_logic.trigger_jumpscare(0.7)
            st.rerun()
        
        st.markdown("---")
        
        # 공포 수치 설명
        with st.expander("📈 공포 시스템 설명"):
            st.markdown("""
            ### 공포 메커니즘
            
            **정신력 (🧠):**
            - 100%: 안정적
            - 50%: 불안정, 환각 가능성
            - 30%: 극도로 취약, 자주 점프스케어
            - 0%: 정신 붕괴, 게임 오버
            
            **공포 지수 (😨):**
            - 0-30: 안정
            - 30-60: 불안 (가벼운 효과)
            - 60-80: 공포 (강한 효과)
            - 80-100: 공황 (극한 효과)
            
            **위험도 표시:**
            - 😨: 낮은 위험
            - 😨😨: 중간 위험
            - 😨😨😨: 높은 위험
            """)
    
    # 메인 게임 영역
    game_container = st.container()
    
    with game_container:
        # 공포 효과 업데이트
        game_logic.update_fear_effects()
        
        # 점프스케어 렌더링
        game_ui.render_jumpscare()
        
        # 깜빡임 효과
        game_ui.render_flicker_effect()
        
        # 심장박동 효과
        game_ui.render_heartbeat_effect()
        
        # 웨이브 효과 (높은 공포 상태)
        if st.session_state.fear > 70:
            st.markdown('<div class="wave-effect"></div>', unsafe_allow_html=True)
        
        # 게임 오버/승리 체크
        if hasattr(st.session_state, 'game_won') and st.session_state.game_won:
            st.balloons()
            st.success("🎉 공포를 이겨냈습니다!")
            st.markdown("""
            ### 공포의 던전 탈출!
            
            당신은 무시무시한 악몽을 극복하고 살아남았습니다.
            하지만 정말로 탈출한 걸까요...?
            
            **최종 기록:**
            - 최종 정신력: {}%
            - 최종 공포 지수: {}%
            - 획득한 공포 증거: {}개
            - 트라우마 기억: {}개
            
            **엔딩 평가:**
            {}
            """.format(
                st.session_state.sanity,
                st.session_state.fear,
                len(st.session_state.inventory),
                len(st.session_state.traumatic_memories),
                "🎭 정신이 망가졌지만 살아남음" if st.session_state.sanity < 30 else
                "👁️‍🗨️ 새로운 진실을 발견함" if len(st.session_state.inventory) >= 3 else
                "🏃 공포에서 도망침" if st.session_state.fear > 80 else
                "🧠 이성으로 공포를 극복함"
            ))
            
            if st.button("💀 다시 공포에 도전한다"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            return
        
        if st.session_state.sanity <= 0:
            st.error("💀 정신 붕괴!")
            st.markdown("""
            ### 정신이 파괴되었습니다...
            
            당신은 더 이상 현실과 환상을 구분할 수 없게 되었습니다.
            공포가 당신을 삼켰고, 영원히 이 던전에 갇히게 되었습니다.
            
            **최후의 기록:**
            - 위치: {}
            - 공포 지수: {}%
            - 트라우마: {}
            - 마지막 메시지: "{}"
            
            *어둠이 당신을 기다리고 있습니다...*
            """.format(
                st.session_state.current_room,
                st.session_state.fear,
                ", ".join(st.session_state.traumatic_memories[-3:]) if st.session_state.traumatic_memories else "없음",
                st.session_state.messages[0]["text"] if st.session_state.messages else "침묵..."
            ))
            
            if st.button("😱 다시 시도 (용감한 자만)"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            return
        
        if st.session_state.health <= 0:
            st.error("🩸 사망!")
            st.markdown("""
            ### 육체가 파괴되었습니다...
            
            상처와 공포가 당신을 쓰러뜨렸습니다.
            이제 당신도 이 던전의 일부가 되었습니다.
            
            **사망 원인:**
            - 위치: {}
            - 남은 정신력: {}%
            - 치명적 선택: {}
            
            *다음 희생자가 당신의 자리를 차지할 때까지...*
            """.format(
                st.session_state.current_room,
                st.session_state.sanity,
                "위험한 실험" if "실험실" in st.session_state.current_room else
                "과감한 대결" if "최종 방" in st.session_state.current_room else
                "무모한 탐험"
            ))
            
            if st.button("👻 유령이 되어 복수한다"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            return
        
        # 게임 화면
        flicker_class = " flicker" if st.session_state.flicker_active else ""
        st.markdown(f'<div class="game-screen{flicker_class}">', unsafe_allow_html=True)
        
        # 방 렌더링
        game_ui.render_room()
        
        # 퍼즐 렌더링 (간단화)
        if st.session_state.show_puzzle:
            room = st.session_state.current_room
            puzzle = game_data.rooms[room]["puzzle"]
            
            st.markdown('<div class="puzzle-window">', unsafe_allow_html=True)
            st.markdown(f"### 💀 {room}의 저주받은 퍼즐")
            st.markdown(f"**{puzzle['question']}**")
            st.markdown(f"*{puzzle['hint']}*")
            
            if puzzle["type"] == "blood_sequence":
                st.write("순서를 맞춰보세요...")
                if st.button("어둠의 순서 시도"):
                    # 실제 구현에서는 더 복잡한 로직
                    game_logic.solve_puzzle("blood_sequence", puzzle["answer"])
                    
            elif puzzle["type"] == "scream_lock":
                code = st.text_input("공포의 숫자를 입력하세요...", max_chars=4, type="password")
                if st.button("자물쇠를 연다 (위험)"):
                    game_logic.solve_puzzle("scream_lock", code)
                    
            if st.button("포기하고 도망친다"):
                st.session_state.show_puzzle = False
                game_logic.add_message("퍼즐을 포기했습니다... 뒤에서 무언가가 다가옵니다.", "horror", 0.4)
                
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 메시지 렌더링
        if st.session_state.messages:
            st.markdown("### 📜 공포의 기록")
            for msg in st.session_state.messages[:5]:
                msg_class = {
                    "horror": "game-message",
                    "warning": "game-message",
                    "success": "game-message",
                    "error": "game-message",
                    "info": "game-message"
                }.get(msg["type"], "game-message")
                
                st.markdown(f'<div class="{msg_class}">[{msg["time"]}] {msg["text"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 자동 새로고침 (공포 효과)
        time.sleep(0.1)
        if random.random() < 0.1 and st.session_state.fear > 40:
            st.rerun()
    
    # 푸터
    st.markdown("""
    <div class="footer">
    <hr>
    <p>💀 © 2024 공포의 방탈출 게임 | 경고: 이 게임은 가상입니다. 실제 공포를 경험하지 마세요.</p>
    <p>🎭 모든 공포는 당신의 마음이 만들어 낸 것입니다...</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
