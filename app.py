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

    # ⏳ 初始時間與生命設定
    st.session_state.time_limit = float("inf")  
    st.session_state.start_time = None
    st.session_state.lives = float("inf")  

    # 👹 怪物模式與 QTE 專用狀態
    st.session_state.monster_active = False  
    st.session_state.monster_type = ""
    st.session_state.qte_1_clicked = False
    st.session_state.qte_2_clicked = False


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
    st.session_state.time_limit = 60
    st.session_state.start_time = time.time()  
    st.session_state.lives = float("inf")


def init_reverse_mode():
    st.session_state.secret_number = random.randint(-999, 100)
    st.session_state.min_val = -999
    st.session_state.max_val = 100
    st.session_state.mode_color = "blue"
    st.session_state.time_limit = 60
    st.session_state.start_time = time.time()
    st.session_state.lives = float("inf")


def init_chaos_mode():
    st.session_state.secret_number = random.randint(-999, 999)
    st.session_state.min_val = -999
    st.session_state.max_val = 999
    st.session_state.mode_color = "orange"
    st.session_state.time_limit = 60
    st.session_state.start_time = time.time()
    st.session_state.lives = float("inf")


# 👹 1x1x1x1 模式：生命 12，加入長條雙綠條 QTE 防禦機制！
def init_monster_mode():
    st.session_state.secret_number = random.randint(1, 110)  
    st.session_state.min_val = 1
    st.session_state.max_val = 110  
    st.session_state.mode_color = "green"  
    st.session_state.monster_active = True
    st.session_state.monster_type = random.choice(["實驗體-01", "未知生命體", "1x1x1x1觀測者"])
    st.session_state.time_limit = 60
    st.session_state.start_time = time.time()
    st.session_state.lives = 12.0  # 支援扣 0.5 滴血
    st.session_state.qte_1_clicked = False
    st.session_state.qte_2_clicked = False


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
        st.markdown(f"### 🟢 **【1x1x1x1 綠色警戒】猜測機會：`inf` | 剩餘護盾：` {st.session_state.lives} / 12 `**")
        st.progress(max(0.0, min(st.session_state.lives / 12.0, 1.0)))
    else:
        st.markdown(f"### ⏳ **猜測機會：`inf` (無限次)**")

    # 🟢 🟢 核心 QTE 機制渲染區
    if st.session_state.mode_color == "green" and st.session_state.monster_active:
        st.error(f"🚨 **[生物突襲] {st.session_state.monster_type} 正在瘋狂撕咬防線！**")
        
        # 視覺長條圖
        st.markdown("**【防禦解鎖進度條】**")
        qte_progress = 0.0
        if st.session_state.qte_1_clicked: qte_progress += 0.5
        if st.session_state.qte_2_clicked: qte_progress += 0.5
        st.progress(qte_progress)

        # 渲染兩個綠色小條（安全按鈕）
        q_col1, q_col2, q_col3 = st.columns([1, 1, 2])
        
        with q_col1:
            if not st.session_state.qte_1_clicked:
                if st.button("🟢 安全鎖 A (點擊)", key="qte_a", use_container_width=True):
                    st.session_state.qte_1_clicked = True
                    st.rerun()
            else:
                st.button("✅ 鎖定成功", key="qte_a_dis", disabled=True, use_container_width=True)

        with q_col2:
            if not st.session_state.qte_2_clicked:
                if st.button("🟢 安全鎖 B (點擊)", key="qte_b", use_container_width=True):
                    st.session_state.qte_2_clicked = True
                    st.rerun()
            else:
                st.button("✅ 鎖定成功", key="qte_b_dis", disabled=True, use_container_width=True)
                
        with q_col3:
            if st.button("🏃‍♂️ 完美迴避 (解鎖後點擊)", key="qte_submit", variant="primary", use_container_width=True):
                # 判定按到了幾個綠色小條
                clicked_count = sum([st.session_state.qte_1_clicked, st.session_state.qte_2_clicked])
                
                if clicked_count == 2:
                    st.success("✨ 完美迴避！成功無傷躲開怪物！")
                elif clicked_count == 1:
                    st.session_state.lives -= 0.5
                    st.warning("⚠️ 擦傷！僅解開一個綠條，護盾扣除 0.5 滴血！")
                else:
                    st.session_state.lives -= 1.0
                    st.error("💥 慘敗！完全沒解開綠條，護盾扣除 1.0 滴血！")
                
                # 重置 QTE 狀態並重整
                st.session_state.monster_active = False
                st.session_state.qte_1_clicked = False
                st.session_state.qte_2_clicked = False
                
                if st.session_state.lives <= 0:
                    st.error("💥 護盾已被完全撕裂，挑戰失敗！")
                    init_normal_mode()
                st.rerun()

    st.markdown("---")

    # 遊戲輸入表單
    with st.form(key="guess_form", clear_on_submit=True):
        player_name = st.text_input("請輸入你的暱稱：", value="匿名玩家")
        guess_input = st.text_input("請輸入你的猜測：", placeholder="填入數字...")
        submit_button = st.form_submit_button(label="確認送出")

    if submit_button:
        user_action = guess_input.strip()

        if st.session_state.start_time is None and st.session_state.time_limit != float("inf"):
            st.session_state.start_time = time.time()
            st.rerun()

        # 如果怪物還在卻直接強行猜數字，視同 QTE 完全失敗，直接扣 1 滴血
        if st.session_state.mode_color == "green" and st.session_state.monster_active:
            st.session_state.lives -= 1.0
            st.error(f"💥 忽視警告！遭到 {st.session_state.monster_type} 正面重擊，扣除 1 滴血！")
            st.session_state.monster_active = False
            st.session_state.qte_1_clicked = False
            st.session_state.qte_2_clicked = False
            if st.session_state.lives <= 0:
                init_normal_mode()
            st.rerun()

        try:
            guess = int(user_action)
            st.session_state.guess_count += 1

            # 彩蛋觸發區
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

            # 檢查範圍
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
                else:
                    st.session_state.min_val = guess
                st.rerun()

        except ValueError:
            if st.session_state.mode_color == "green":
                st.session_state.lives -= 1.0
                st.error("💥 核心資料格式出錯，系統精神反噬扣除 1 滴血。")
                if st.session_state.lives <= 0:
                    init_normal_mode()
                st.rerun()
            else:
                st.error("❌ 請輸入正確的數字。")

        # 🟢 猜完之後刷新下一波怪物與 QTE
        if st.session_state.mode_color == "green" and not st.session_state.game_cleared:
            st.session_state.monster_active = True
            st.session_state.monster_type = random.choice(["實驗體-01", "未知生命體", "1x1x1x1觀測者"])
            st.session_state.qte_1_clicked = False
            st.session_state.qte_2_clicked = False
            st.rerun()

    if st.session_state.game_cleared:
        st.warning("🎁 **【隱藏彩蛋解鎖】第一猜輸入 666 即可開啟 1x1x1x1 雙綠條極限生存戰！**")

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
