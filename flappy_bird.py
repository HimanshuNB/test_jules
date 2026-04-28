import streamlit as st
import time
import random

# Initialize session state for game variables
if 'bird_y' not in st.session_state:
    st.session_state.bird_y = 50
if 'bird_velocity' not in st.session_state:
    st.session_state.bird_velocity = 0
if 'pipes' not in st.session_state:
    st.session_state.pipes = [{'x': 100, 'height': 30}]
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

st.title("Flappy Bird in Streamlit")

# Constants
GRAVITY = 2
JUMP_STRENGTH = -15
PIPE_SPEED = 5
PIPE_WIDTH = 10
GAP_SIZE = 30
BIRD_SIZE = 5
MAX_Y = 100

def reset_game():
    st.session_state.bird_y = 50
    st.session_state.bird_velocity = 0
    st.session_state.pipes = [{'x': 100, 'height': random.randint(20, MAX_Y - GAP_SIZE - 20)}]
    st.session_state.score = 0
    st.session_state.game_over = False

# Controls
col1, col2 = st.columns(2)
with col1:
    if st.button("Jump (Press Space)", key="jump_btn"):
        if not st.session_state.game_over:
            st.session_state.bird_velocity = JUMP_STRENGTH
with col2:
    if st.button("Restart"):
        reset_game()

# Game Loop (using a placeholder to update)
game_area = st.empty()

def draw_game():
    if st.session_state.game_over:
        return f"""
        <div style="width: 400px; height: 400px; background-color: #87CEEB; position: relative; border: 2px solid black;">
            <h2 style="text-align: center; color: red; margin-top: 150px;">GAME OVER</h2>
            <h3 style="text-align: center;">Score: {st.session_state.score}</h3>
        </div>
        """

    bird_y_px = (st.session_state.bird_y / MAX_Y) * 400

    html = f"""
    <div style="width: 400px; height: 400px; background-color: #87CEEB; position: relative; border: 2px solid black; overflow: hidden;">
        <!-- Bird -->
        <div style="position: absolute; left: 50px; top: {bird_y_px}px; width: 20px; height: 20px; background-color: yellow; border-radius: 50%;"></div>
    """

    for pipe in st.session_state.pipes:
        pipe_x_px = (pipe['x'] / 100) * 400
        top_height_px = (pipe['height'] / MAX_Y) * 400
        bottom_y_px = ((pipe['height'] + GAP_SIZE) / MAX_Y) * 400
        bottom_height_px = 400 - bottom_y_px

        # Top pipe
        html += f"""
        <div style="position: absolute; left: {pipe_x_px}px; top: 0; width: {PIPE_WIDTH / 100 * 400}px; height: {top_height_px}px; background-color: green;"></div>
        """
        # Bottom pipe
        html += f"""
        <div style="position: absolute; left: {pipe_x_px}px; top: {bottom_y_px}px; width: {PIPE_WIDTH / 100 * 400}px; height: {bottom_height_px}px; background-color: green;"></div>
        """

    html += f"""
        <div style="position: absolute; top: 10px; left: 10px; font-size: 24px; font-weight: bold; color: white;">Score: {st.session_state.score}</div>
    </div>
    """
    return html

def update_game_state():
    if st.session_state.game_over:
        return

    # Update bird physics
    st.session_state.bird_velocity += GRAVITY
    st.session_state.bird_y += st.session_state.bird_velocity

    # Check floor/ceiling collision
    if st.session_state.bird_y >= MAX_Y or st.session_state.bird_y <= 0:
        st.session_state.game_over = True
        return

    # Update pipes
    for pipe in st.session_state.pipes:
        pipe['x'] -= PIPE_SPEED

        # Check collision
        bird_rect = {'x': 12.5, 'y': st.session_state.bird_y, 'w': BIRD_SIZE, 'h': BIRD_SIZE} # approx bird width 5%
        pipe_rect_top = {'x': pipe['x'], 'y': 0, 'w': PIPE_WIDTH, 'h': pipe['height']}
        pipe_rect_bottom = {'x': pipe['x'], 'y': pipe['height'] + GAP_SIZE, 'w': PIPE_WIDTH, 'h': MAX_Y - (pipe['height'] + GAP_SIZE)}

        # Collision logic
        if bird_rect['x'] + bird_rect['w'] > pipe_rect_top['x'] and bird_rect['x'] < pipe_rect_top['x'] + pipe_rect_top['w']:
            if bird_rect['y'] < pipe_rect_top['h'] or bird_rect['y'] + bird_rect['h'] > pipe_rect_bottom['y']:
                st.session_state.game_over = True
                return

        # Score update
        if pipe['x'] == 10: # Passed the bird
            st.session_state.score += 1

    # Remove off-screen pipes and add new ones
    if st.session_state.pipes[0]['x'] < -PIPE_WIDTH:
        st.session_state.pipes.pop(0)

    if len(st.session_state.pipes) == 0 or st.session_state.pipes[-1]['x'] < 50:
        new_height = random.randint(20, MAX_Y - GAP_SIZE - 20)
        st.session_state.pipes.append({'x': 100, 'height': new_height})

# Auto-refresh using experimental_rerun loop for animation effect
if not st.session_state.game_over:
    update_game_state()
    game_area.markdown(draw_game(), unsafe_allow_html=True)
    time.sleep(0.1)
    st.rerun()
else:
    game_area.markdown(draw_game(), unsafe_allow_html=True)
