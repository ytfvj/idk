import random
import time
import pandas as pd
import streamlit as st

# ==========================================
# 1. 網頁基本設定
# ==========================================
st.set_page_config(
    page_title="終極密碼：時空局限版", page_icon="⏳", layout="wide"
)

st.title("🔢 終極密碼：時空局限版")

# 初始化遊戲狀態
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.min_val = 1
    st.session_state.max_val = 100
    st.session_state.mode_color = "black"
    st.session_state.guess_count = 0
    st.session_state.game_cleared = False
    st.session_state.leaderboard = []

    # ⏳ 初始時間與生命設定（普通模式時間無限）
    st.session_state.time_limit = float("inf")  
    st.session_state.start_time = None
    st.session_state.lives = float("inf")  

    # 👹 怪物模式專用狀態
    st.session_state.monster_active = False  
    st.session_state.monster_type = ""


# 各模式初始化功能
def init_normal_mode():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.min_val = 1
    st.session_state.max_val = 100
    st.session_state.mode_color = "black"
    st.session_state.guess_count = 0
    st.session_state.game_cleared = False
    st.session_state.monster_active = False
    st.session_state.time_limit = float("inf") 
    st.session_state.start_time = None
    st.session_state.lives = float("inf")


def init_hell_mode():
    st.session_state.secret_number = random.randint(1, 999)
    st.session_state.min_val = 1
    st.session_state.max_val = 999
    st.session_state.mode_color = "purple"
    st.session_state.game_msg = "已進入地獄模式。時間限制 60 秒，機會無限。"
    st.session_state.time_limit = 60
    st.session_state.start_time = time.time()  
    st.session_state.lives = float("inf")


def init_reverse_mode():
    st.session_state.secret_number = random.randint(-999, 100)
    st.session_state.min_val = -999
    st.session_state.max_val = 100
    st.session_state.mode_color = "blue"
    st.session_state.game_msg = "已進入顛倒世界。時間限制 60 秒，機會無限。"
    st.session_state.time_limit = 60
    st.session_state.start_time = time.time()
    st.session_state.lives = float("inf")


def init_chaos_mode():
    st.session_state.secret_number = random.randint(-999, 999)
    st.session_state.min_val = -999
    st.session_state.max_val = 999
    st.session_state.mode_color = "orange"
    st.session_state.game_msg = "已進入混沌宇宙。時間限制 60 秒，機會無限。"
    st.session_state.time_limit = 60
    st.session_state.start_time = time.time()
    st.session_state.lives = float("inf")


# 👹 1x1x1x1 模式：範圍 1 ~ 110，【答案保密】，考驗一邊猜測、一邊按 R 閃避
def init_monster_mode():
    st.session_state.secret_number = random.randint(1, 110)  
    st.session_state.min_val = 1
    st.session_state.max_val = 110  
    st.session_state.mode_color = "green"  
    st.session_state.monster_active = True
    st.session_state.monster_type = random.choice(["實驗體-01", "未知生命體", "1x1x1x1觀測者"])
    st.session_state.game_msg = "已進入 1x1x1x1 模式。範圍 1 ~ 110。密碼已完全加密，請在躲避生物（按 R）的同時進行猜測！"
    st.session_state.time_limit = 60
    st.session_state.start_time = time.time()
    st.session_state.lives = 3


# ==========================================
# 2. 計算與檢查剩餘時間
# ==========================================
time_left_str = "無限制"
if st.session_state.start_time is not None and not st.session_state.game_cleared:
    if st.session_state.time_limit != float("inf"):
        elapsed = time.time() - st.session_state.start_time
        time_left = max(0, int(st.session_state.time_limit - elapsed))
        time_left_str = f"{time_left} 秒"

        if time_left <= 0:
            st.error(f"⌛ 時間耗盡！系統已強制重置。正確答案曾是：{st.session_state.secret_number}")
            init_normal_mode()
            st.rerun()


# ==========================================
# 3. 網頁版面配置
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎮 遊戲區")

    # 顯示目前範圍
    st.subheader(f"目前範圍： :blue[{st.session_state.min_val}] ~ :red[{st.session_state.max_val}]")

    # 狀態面板
    st.markdown(f"### ⏳ **剩餘時間：{time_left_str}**")
    
    if st.session_state.mode_color == "green":
        st.markdown(f"### 🟢 **【1x1x1x1 綠色警戒】猜測機會：`inf` | 生命防護：{'❤️' * st.session_state.lives}**")
    else:
        st.markdown(f"### ⏳ **猜測機會：`inf` (無限次)**")

    # 🟢 綠色警戒機制（移除 st.code 密碼明牌顯示）
    if st.session_state.mode_color == "green":
        if st.session_state.monster_active:
            st.success(
                f"🟢 **[綠色警戒] 生物突襲警告：{st.session_state.monster_type} 已接近。**\n\n"
                "請先在下方按下「按 R 避開」或輸入 R 送出。若直接進行數字猜測將會受到攻擊。"
            )

            if st.button("🏃‍♂️ 按 R 避開", key="r_button"):
                st.success(f"確認迴避。已成功避開 {st.session_state.monster_type}。")
                st.session_state.monster_active = False  
                st.rerun()

    st.markdown("---")

    # 遊戲輸入表單
    with st.form(key="guess_form", clear_on_submit=True):
        player_name = st.text_input("請輸入你的暱稱：", value="匿名玩家")
        guess_input = st.text_input("請輸入你的猜測（或輸入 R 進行閃避）：", placeholder="填入數字或指令...")
        submit_button = st.form_submit_button(label="確認送出")

    if submit_button:
        user_action = guess_input.strip()

        if st.session_state.start_time is None and st.session_state.time_limit != float("inf"):
            st.session_state.start_time = time.time()
            st.rerun()

        # 處理綠色警戒模式下的行動
        if st.session_state.mode_color == "green":
            if user_action.upper() == "R":
                if st.session_state.monster_active:
                    st.success(f"確認迴避。已成功避開 {st.session_state.monster_type}。")
                    st.session_state.monster_active = False
                else:
                    st.warning("目前並未偵測到生物威脅。")
                st.rerun()

            elif st.session_state.monster_active:
                st.session_state.lives -= 1
                st.error(f"迴避失敗。受到 {st.session_state.monster_type} 攻擊，扣除一條命。")
                st.session_state.monster_active = False

                if st.session_state.lives <= 0:
                    st.error("防護已歸零，系統判定強制終止。")
                    init_normal_mode()
                st.rerun()

        try:
            guess = int(user_action)
            st.session_state.guess_count += 1

            # 彩蛋觸發區（必須在未變動的 1~100 初始狀態下）
            if st.session_state.min_val == 1 and st.session_state.max_val == 100 and st.session_state.mode_color == "black":
                if guess == 999:
                    init_hell_mode()
                    st.rerun()
                elif guess == -999:
                    init_reverse_mode()
                    st.rerun()
                elif guess == 1000:
                    init_chaos_mode()
                    st.rerun()
                elif guess == 666:
                    init_monster_mode()
                    st.rerun()

            # 🛑 核心檢查：如果輸入超出範圍
            if guess < st.session_state.min_val or guess > st.session_state.max_val:
                st.warning(f"注意：請輸入 {st.session_state.min_val} 到 {st.session_state.max_val} 之間的數字。")
                st.rerun()

            # 猜對了
            if guess == st.session_state.secret_number:
                st.balloons()
                st.session_state.game_cleared = True
                
                if st.session_state.start_time is not None:
                    elapsed_time = round(time.time() - st.session_state.start_time, 2)
                else:
                    elapsed_time = "無限制模式"

                current_mode_name = "一般"
                if st.session_state.mode_color == "purple": current_mode_name = "地獄"
                elif st.session_state.mode_color == "blue": current_mode_name = "顛倒"
                elif st.session_state.mode_color == "orange": current_mode_name = "混沌"
                elif st.session_state.mode_color == "green": current_mode_name = "🟢1x1x1x1"

                st.success(f"通關成功！密碼為 {st.session_state.secret_number}。\n\n⏱️ 耗時：{elapsed_time} | 🎯 行動次數：{st.session_state.guess_count} 次")

                st.session_state.leaderboard.append({
                    "玩家": player_name, "模式": current_mode_name, "耗時 (秒)": elapsed_time if type(elapsed_time)==float else 999, "次數 (次)": st.session_state.guess_count
                })
                init_normal_mode()
                st.session_state.game_cleared = True

            # 猜錯了
            else:
                if guess > st.session_state.secret_number:
                    st.session_state.max_val = guess
                    st.session_state.game_msg = "提示：偏大。"
                else:
                    st.session_state.min_val = guess
                    st.session_state.game_msg = "提示：偏小。"
                st.rerun()

        except ValueError:
            if st.session_state.mode_color == "green":
                st.session_state.lives -= 1
                st.error("輸入格式錯誤，防護受到未知精神干擾，扣除一條命。")
                if st.session_state.lives <= 0:
                    init_normal_mode()
                st.rerun()
            else:
                st.error("❌ 請輸入正確的數字。")

        # 🟢 綠色警戒專用生物刷新機制
        if st.session_state.mode_color == "green" and not st.session_state.game_cleared:
            st.session_state.monster_active = True
            st.session_state.monster_type = random.choice(["實驗體-01", "未知生命體", "1x1x1x1觀測者"])
            st.rerun()

    if st.session_state.game_cleared:
        st.warning(
            "🎁 **【通關隱藏彩蛋解鎖】**\n\n"
            "已確認以下平行宇宙入口指令，可於一般模式第一猜輸入：\n"
            "* 輸入 **999** ➡️ 進入【地獄模式 (1 ~ 999)】(限時60秒)\n"
            "* 輸入 **-999** ➡️ 進入【顛倒世界 (-999 ~ 100)】(限時60秒)\n"
            "* 輸入 **1000** ➡️ 進入【混沌宇宙 (-999 ~ 999)】(限時60秒)\n"
            "* 輸入 **666** ➡️ 進入【1x1x1x1 綠色警戒】(限時60秒，範圍 1 ~ 110 加密盲猜，無限次機會但僅有 3 條命，需配合 R 鍵迴避)"
        )

    if st.button("重新開始遊戲"):
        init_normal_mode()
        st.rerun()

# --- 右側：榮譽排行榜區 ---
with col2:
    st.header("🏆 榮譽排行榜 (Top 15)")
    if len(st.session_state.leaderboard) > 0:
        df = pd.DataFrame(st.session_state.leaderboard)
        tab1, tab2 = st.tabs(["⏱️ 時間最快", "🎯 次數最少"])
        with tab1:
            st.subheader("⏱️ 秒數神速榜")
            df_time = df.sort_values(by="耗時 (秒)").head(15).reset_index(drop=True)
            df_time.index = df_time.index + 1
            st.dataframe(df_time, use_container_width=True)
        with tab2:
            st.subheader("🎯 精準次數榜")
            df_count = df.sort_values(by="次數 (次)").head(15).reset_index(drop=True)
            df_count.index = df_count.index + 1
            st.dataframe(df_count, use_container_width=True)
    else:
        st.info("目前尚無紀錄。")

