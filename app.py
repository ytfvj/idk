import random
import pandas as pd
import streamlit as st

# ==========================================
# 1. 網頁基本設定（已移除「時空」字眼）
# ==========================================
st.set_page_config(
    page_title="終極密碼", page_icon="🔢", layout="wide"
)

st.title("🔢 終極密碼")

# 初始化遊戲狀態
if "secret_number" not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.min_val = 1
    st.session_state.max_val = 100
    st.session_state.mode_color = "black"
    st.session_state.guess_count = 0
    st.session_state.game_cleared = False
    st.session_state.leaderboard = []

    # 🎯 初始設定猜測次數
    st.session_state.max_guesses = float("inf")  # 一般模式無限次


# 各模式初始化功能（已全面拔除時間與計時狀態）
def init_normal_mode():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.min_val = 1
    st.session_state.max_val = 100
    st.session_state.mode_color = "black"
    st.session_state.guess_count = 0
    st.session_state.game_cleared = False
    st.session_state.max_guesses = float("inf")


def init_hell_mode():
    st.session_state.secret_number = random.randint(1, 999)
    st.session_state.min_val = 1
    st.session_state.max_val = 999
    st.session_state.mode_color = "purple"
    st.session_state.guess_count = 0
    st.session_state.game_cleared = False
    st.session_state.max_guesses = float("inf")


def init_reverse_mode():
    st.session_state.secret_number = random.randint(-999, 100)
    st.session_state.min_val = -999
    st.session_state.max_val = 100
    st.session_state.mode_color = "blue"
    st.session_state.guess_count = 0
    st.session_state.game_cleared = False
    st.session_state.max_guesses = float("inf")


def init_chaos_mode():
    st.session_state.secret_number = random.randint(-999, 999)
    st.session_state.min_val = -999
    st.session_state.max_val = 999
    st.session_state.mode_color = "orange"
    st.session_state.guess_count = 0
    st.session_state.game_cleared = False
    st.session_state.max_guesses = float("inf")


# 👹 1x1x1x1 模式：無時間限制，嚴格限制 8 次猜測機會！
def init_monster_mode():
    st.session_state.secret_number = random.randint(1, 110)  
    st.session_state.min_val = 1
    st.session_state.max_val = 110  
    st.session_state.mode_color = "green"  
    st.session_state.guess_count = 0
    st.session_state.game_cleared = False
    st.session_state.max_guesses = 8  # 🎯 限制 8 次機會


# ==========================================
# 2. 網頁版面配置
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🎮 遊戲區")

    # 顯示目前範圍
    st.subheader(f"目前範圍： :blue[{st.session_state.min_val}] ~ :red[{st.session_state.max_val}]")

    # 狀態面板（已徹底移除時間文字顯示）
    if st.session_state.mode_color == "green":
        # 計算與顯示剩餘幾次機會
        guesses_left = st.session_state.max_guesses - st.session_state.guess_count
        st.markdown(f"### 🎯 **【1x1x1x1 模式】剩餘機會：:red[{guesses_left} / 8] 次**")
        st.progress(guesses_left / 8.0)
    else:
        st.markdown(f"### 🎯 **目前已猜次數：{st.session_state.guess_count} 次**")
        
    st.markdown("---")

    # 遊戲輸入表單
    with st.form(key="guess_form", clear_on_submit=True):
        player_name = st.text_input("請輸入你的暱稱：", value="匿名玩家")
        guess_input = st.text_input("請輸入你的猜測：", placeholder="填入數字...")
        submit_button = st.form_submit_button(label="確認送出")

    if submit_button:
        user_action = guess_input.strip()

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

            # 檢查範圍
            if guess < st.session_state.min_val or guess > st.session_state.max_val:
                st.warning(f"注意：請輸入 {st.session_state.min_val} 到 {st.session_state.max_val} 之間的數字。")
                # 超出範圍一樣算猜錯，檢查次數
                if st.session_state.guess_count >= st.session_state.max_guesses:
                    st.error(f"💥 次數耗盡！挑戰失敗。正確答案曾是：{st.session_state.secret_number}")
                    init_normal_mode()
                st.rerun()

            # 猜對了
            if guess == st.session_state.secret_number:
                st.balloons()
                st.session_state.game_cleared = True
                
                st.success(f"通關成功！密碼為 {st.session_state.secret_number}。\n\n🎯 總共花費次數：{st.session_state.guess_count} 次！")

                # 排行榜欄位同步拔除耗時，只保留次數
                st.session_state.leaderboard.append({
                    "玩家": player_name, 
                    "模式": "🟢1x1x1x1" if st.session_state.mode_color == "green" else "一般", 
                    "次數 (次)": st.session_state.guess_count
                })
                init_normal_mode()
                st.session_state.game_cleared = True

            # 猜錯了
            else:
                # 檢查次數是否用完了
                if st.session_state.guess_count >= st.session_state.max_guesses:
                    st.error(f"💥 次數耗盡！挑戰失敗。正確答案曾是：{st.session_state.secret_number}")
                    init_normal_mode()
                    st.rerun()
                
                if guess > st.session_state.secret_number:
                    st.session_state.max_val = guess
                else:
                    st.session_state.min_val = guess
                st.rerun()

        except ValueError:
            st.error("❌ 請輸入正確的數字。")

    if st.button("重新開始遊戲"):
        init_normal_mode()
        st.rerun()

# --- 右側：榮譽排行榜區（完全移除時間排行） ---
with col2:
    st.header("🏆 榮譽排行榜 (Top 15)")
    if len(st.session_state.leaderboard) > 0:
        df = pd.DataFrame(st.session_state.leaderboard)
        st.subheader("🎯 精準次數榜")
        df_count = df.sort_values(by="次數 (次)").head(15).reset_index(drop=True)
        df_count.index = df_count.index + 1
        st.dataframe(df_count, use_container_width=True)
    else:
        st.info("目前尚無紀錄。")
