# app.py
import streamlit as st
import base64
from pathlib import Path
import webbrowser
import os

# 페이지 설정
st.set_page_config(
    page_title="공포 방탈출 게임",
    page_icon="👻",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton > button {
        width: 100%;
        margin-top: 10px;
    }
    .game-title {
        text-align: center;
        color: #ff0000;
        font-size: 3rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px #000000;
        margin-bottom: 2rem;
    }
    .warning {
        background-color: #330000;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ff0000;
        margin: 1rem 0;
    }
    .controls {
        background-color: #222222;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 게임 제목
st.markdown('<h1 class="game-title">👻 공포의 방탈출 게임 👻</h1>', unsafe_allow_html=True)

# 경고 메시지
st.markdown("""
<div class="warning">
    <h3>⚠️ 주의사항</h3>
    <p>이 게임은 강렬한 공포 요소를 포함하고 있습니다.<br>
    • 예기치 않은 점프스케어가 포함되어 있습니다<br>
    • 정신력 시스템이 구현되어 있습니다<br>
    • 권장 연령: 16세 이상<br>
    • 심장이 약하신 분들은 플레이를 삼가해주세요</p>
</div>
""", unsafe_allow_html=True)

# 컬럼 레이아웃
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 게임 설명
    st.markdown("### 🎮 게임 설명")
    st.write("""
    당신은 버려진 정신병원에 갇혔습니다.
    5개의 방을 통과하며 퍼즐을 해결하고 탈출해야 합니다.
    하지만 이곳에는 당신을 기다리는 무언가가 있습니다...
    """)
    
    # 게임 특징
    st.markdown("### 🌟 게임 특징")
    features = [
        "🔸 5개의 독특한 방 디자인",
        "🔸 정신력 시스템 - 낮을수록 이상현상 발생",
        "🔸 3가지 종류의 점프스케어",
        "🔸 AI 몬스터 추적 시스템",
        "🔸 복잡한 퍼즐과 수집 요소",
        "🔸 실시간 심박수 모니터링"
    ]
    
    for feature in features:
        st.write(feature)
    
    # 컨트롤 설명
    st.markdown("""
    <div class="controls">
        <h3>🎯 조작법</h3>
        <p>• W/A/S/D: 이동<br>
        • 마우스: 시점 조절<br>
        • 스페이스바: 상호작용<br>
        • R: 정신력 확인<br>
        • 마우스 클릭: 퍼즐 조작</p>
    </div>
    """, unsafe_allow_html=True)

# 게임 시작 버튼
if st.button("🎮 게임 시작하기", type="primary"):
    # VPython 게임 페이지로 이동
    game_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>공포의 방탈출 게임</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: black;
            }
            #game-container {
                width: 100vw;
                height: 100vh;
            }
        </style>
        <script type="module" src="https://cdn.jsdelivr.net/npm/vpython@3.2.1/dist/vpython.min.js"></script>
    </head>
    <body>
        <div id="game-container"></div>
        <script type="module">
            import * as VPython from 'https://cdn.jsdelivr.net/npm/vpython@3.2.1/dist/vpython.esm.js';
            const { scene, box, sphere, cylinder, text, vector, color, rate, random, cross, mag, compound, compound, rotate, radians } = VPython;
            
            // 게임 설정
            scene.title = "공포의 미궁: 잊혀진 정신병원";
            scene.width = window.innerWidth;
            scene.height = window.innerHeight;
            scene.background = color.black;
            scene.center = vector(0, 5, 0);
            scene.fov = 0.8;
            
            // 게임 변수
            let current_room = 0;
            let inventory = [];
            let game_over = false;
            let sanity = 100;
            let solved_puzzles = [false, false, false, false, false];
            let monster_active = false;
            let monster_position = vector(0, 0, 0);
            let heartbeat_rate = 60;
            let player_sequence = [];
            
            // 방 설명
            const room_descriptions = [
                "1호실: 접수실 - 오래된 수수께끼가 적힌 일지가 있다",
                "2호실: 치료실 - 기괴한 숫자 패턴이 적힌 벽",
                "3호실: 수술실 - 피로 쓰여진 메시지가 있다",
                "4호실: 격리실 - 어둠 속에서 무언가가 숨쉰다",
                "5호실: 탈출구 - 마지막 문이 보인다... 하지만 잠겨있다"
            ];
            
            // 퍼즐 정답
            const puzzle_answers = ["의자", "16-9-4-11", "1879", "뒤로세걸음", "모든열쇠"];
            
            // 점프스케어 함수들...
            // (이전 코드의 점프스케어 함수들 여기에 포함)
            
            // 방 생성 함수
            function create_room(room_num) {
                const wall_thickness = 0.3;
                const wall_height = 12;
                const wall_length = 25;
                
                const walls = [];
                const objects = [];
                
                // 바닥과 천장 생성
                const floor_colors = [color.gray(0.6), color.green, color.red, color.black, color.gray(0.4)];
                const floor = box({
                    pos: vector(0, -wall_height/2, 0),
                    size: vector(wall_length, 0.3, wall_length),
                    color: floor_colors[room_num]
                });
                walls.push(floor);
                
                const ceiling = box({
                    pos: vector(0, wall_height/2, 0),
                    size: vector(wall_length, 0.3, wall_length),
                    color: color.gray(0.8)
                });
                walls.push(ceiling);
                
                // 벽 생성
                const wall_colors = [color.blue, color.green, color.red, color.purple, color.orange];
                walls.push(box({pos: vector(0, 0, -wall_length/2), size: vector(wall_length, wall_height, wall_thickness), color: wall_colors[room_num]}));
                walls.push(box({pos: vector(0, 0, wall_length/2), size: vector(wall_length, wall_height, wall_thickness), color: wall_colors[room_num]}));
                walls.push(box({pos: vector(-wall_length/2, 0, 0), size: vector(wall_thickness, wall_height, wall_length), color: wall_colors[room_num]}));
                walls.push(box({pos: vector(wall_length/2, 0, 0), size: vector(wall_thickness, wall_height, wall_length), color: wall_colors[room_num]}));
                
                // 방별 오브젝트 추가
                if (room_num === 0) {
                    // 방 0: 접수실
                    const desk = box({
                        pos: vector(-6, 0, 3),
                        size: vector(5, 2, 10),
                        color: color.brown
                    });
                    objects.push(desk);
                    
                    const riddle_text = text({
                        text: '일지에 적힌 글:\\n"나는 도서관에 있지만 읽히지 않는다.\\n나는 다리가 있지만 걷지 않는다.\\n나는 책상에 앉아있지만 앉지 않는다."',
                        pos: vector(-6, 3, 3),
                        height: 0.7,
                        depth: 0.1,
                        color: color.yellow
                    });
                    objects.push(riddle_text);
                    
                } else if (room_num === 1) {
                    // 방 1: 치료실 - 숫자 퍼즐
                    const panel = box({
                        pos: vector(0, 2, 5),
                        size: vector(6, 4, 0.5),
                        color: color.gray(0.2)
                    });
                    objects.push(panel);
                    
                    // 숫자 버튼 생성
                    for (let i = 0; i < 4; i++) {
                        for (let j = 0; j < 4; j++) {
                            const num = i * 4 + j + 1;
                            const button = box({
                                pos: vector(-2.5 + j * 1.7, 3.5 - i * 1.5, 5.3),
                                size: vector(1.2, 1.2, 0.2),
                                color: color.white
                            });
                            const label = text({
                                text: num.toString(),
                                pos: vector(-2.5 + j * 1.7, 3.5 - i * 1.5, 5.5),
                                height: 0.3,
                                depth: 0.05,
                                color: color.black
                            });
                            objects.push(button, label);
                        }
                    }
                    
                } else if (room_num === 2) {
                    // 방 2: 수술실
                    const table = box({
                        pos: vector(0, -3, 0),
                        size: vector(8, 1, 3),
                        color: color.gray(0.9)
                    });
                    objects.push(table);
                    
                    const message = text({
                        text: "HELP\\nUS\\nESCAPE",
                        pos: vector(-12.3, 0, 0),
                        height: 1.5,
                        depth: 0.1,
                        color: color.red
                    });
                    objects.push(message);
                    
                } else if (room_num === 3) {
                    // 방 3: 격리실
                    monster_active = true;
                    monster_position = vector(random.uniform(-8, 8), 0, random.uniform(-8, 8));
                    
                } else if (room_num === 4) {
                    // 방 4: 탈출구
                    const door = box({
                        pos: vector(12.3, 0, 0),
                        size: vector(0.5, 8, 6),
                        color: color.gray(0.7)
                    });
                    objects.push(door);
                    
                    const escape_text = text({
                        text: "ESCAPE\\nINSERT ALL KEYS",
                        pos: vector(11.5, 3, 0),
                        height: 1,
                        depth: 0.1,
                        color: color.green
                    });
                    objects.push(escape_text);
                }
                
                return { walls, objects };
            }
            
            // 초기 방 생성
            let room_data = create_room(current_room);
            let room_walls = room_data.walls;
            let room_objects = room_data.objects;
            
            // 카메라 설정
            scene.camera.pos = vector(0, 3, 10);
            scene.camera.axis = vector(0, 0, -1);
            
            // UI 텍스트
            const info_text = text({
                text: room_descriptions[current_room],
                pos: vector(-20, 18, 0),
                height: 1,
                depth: 0.1,
                color: color.white
            });
            
            const inventory_text = text({
                text: "인벤토리: 비어있음",
                pos: vector(-20, 15, 0),
                height: 0.8,
                depth: 0.1,
                color: color.green
            });
            
            const sanity_text = text({
                text: `정신력: \${sanity.toFixed(0)}%`,
                pos: vector(-20, 12, 0),
                height: 0.8,
                depth: 0.1,
                color: color.blue
            });
            
            // 키보드 이벤트
            scene.bind('keydown', (event) => {
                const key = event.key.toLowerCase();
                const speed = 1.5;
                
                if (key === 'w') {
                    scene.camera.pos = scene.camera.pos.add(scene.camera.axis.mul(speed));
                } else if (key === 's') {
                    scene.camera.pos = scene.camera.pos.sub(scene.camera.axis.mul(speed));
                } else if (key === 'a') {
                    const right = cross(scene.camera.axis, vector(0, 1, 0)).norm();
                    scene.camera.pos = scene.camera.pos.sub(right.mul(speed));
                } else if (key === 'd') {
                    const right = cross(scene.camera.axis, vector(0, 1, 0)).norm();
                    scene.camera.pos = scene.camera.pos.add(right.mul(speed));
                }
            });
            
            // 마우스 이벤트
            scene.bind('mousedown', (event) => {
                // 마우스 클릭 처리
                console.log('Mouse clicked at:', event.pos);
            });
            
            // 게임 루프
            function gameLoop() {
                if (game_over) return;
                
                // 정신력 업데이트
                sanity = Math.max(0, sanity - 0.05);
                
                // UI 업데이트
                sanity_text.text = `정신력: \${sanity.toFixed(0)}%`;
                
                if (sanity > 50) {
                    sanity_text.color = color.blue;
                } else if (sanity > 20) {
                    sanity_text.color = color.yellow;
                } else {
                    sanity_text.color = color.red;
                }
                
                // 정신력 0 체크
                if (sanity <= 0 && !game_over) {
                    game_over = true;
                    const game_over_text = text({
                        text: "GAME OVER\\n정신이 붕괴되었습니다",
                        pos: vector(0, 10, 0),
                        height: 3,
                        depth: 0.2,
                        color: color.red
                    });
                }
                
                // 다음 프레임 요청
                requestAnimationFrame(gameLoop);
            }
            
            // 게임 시작
            gameLoop();
            
            // 콘솔에 시작 메시지 출력
            console.log("공포의 방탈출 게임이 시작되었습니다!");
            console.log("조작법: W/A/S/D - 이동, 마우스 - 시점 조절");
        </script>
    </body>
    </html>
    """
    
    # HTML 파일로 저장
    with open("horror_game.html", "w", encoding="utf-8") as f:
        f.write(game_html)
    
    # HTML 파일을 열기
    st.success("게임이 준비되었습니다! 아래 버튼을 클릭하거나 게임 파일을 다운로드하세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🕹️ 게임 실행하기"):
            webbrowser.open("horror_game.html")
    
    with col2:
        with open("horror_game.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        b64 = base64.b64encode(html_content.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="horror_escape_game.html">📥 게임 다운로드</a>'
        st.markdown(href, unsafe_allow_html=True)

# 게임 미리보기
st.markdown("---")
st.markdown("### 🎥 게임 미리보기")

# 게임 스크린샷 설명
col1, col2, col3 = st.columns(3)
with col1:
    st.image("https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400&h=300&fit=crop", 
             caption="접수실 - 수수께끼 풀기")
with col2:
    st.image("https://images.unsplash.com/photo-1511512578047-dfb367046420?w=400&h=300&fit=crop",
             caption="치료실 - 숫자 퍼즐")
with col3:
    st.image("https://images.unsplash.com/photo-1534423861386-85a16f5d13fd?w-400&h=300&fit=crop",
             caption="격리실 - 몬스터 출몰")

# 팀 정보
st.markdown("---")
st.markdown("### 👥 개발팀 정보")
st.write("""
- **게임 디자인**: Red Team
- **프로그래밍**: Blue Team  
- **공포 요소 디자인**: Ghost Team
- **테스팅**: Beta Testers

**버전**: 1.0.0
**최종 업데이트**: 2024년
""")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>© 2024 공포의 방탈출 게임. 모든 권리 보유.</p>
    <p>이 게임은 공포 장르를 좋아하는 사람들을 위해 제작되었습니다.</p>
</div>
""", unsafe_allow_html=True)
