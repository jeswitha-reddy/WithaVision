import streamlit as st
import numpy as np
import plotly.graph_objects as go
import re
from PIL import Image
import pytesseract

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(layout="wide")

st.markdown("""
<style>
.stApp {background-color:#0E1117;}
h1,h2,h3,label {color:white;}
button[kind="primary"] {
    background-color:#00FFFF !important;
    color:black !important;
    font-weight:bold !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 WithaVision – Ultimate 3D AI Physics Lab")

# ==========================================================
# SESSION STATE
# ==========================================================
if "score" not in st.session_state:
    st.session_state.score = 0
if "attempts" not in st.session_state:
    st.session_state.attempts = 0

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.title("⚙ Control Panel")

mode_3d = st.sidebar.toggle("Enable Real 3D Mode")
show_vectors = st.sidebar.checkbox("Show Velocity Vector", value=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📘 Formula Memory")

st.sidebar.write("Vertical:")
st.sidebar.write("v = u + at")
st.sidebar.write("s = ut + ½at²")

st.sidebar.write("Projectile:")
st.sidebar.write("Vx = Vcosθ")
st.sidebar.write("Vy = Vsinθ")

# ==========================================================
# OCR UPLOAD
# ==========================================================
uploaded = st.file_uploader("Upload Question Image", type=["png","jpg","jpeg"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, width=350)
    extracted_text = pytesseract.image_to_string(img)
    st.info("Extracted Text:")
    st.write(extracted_text)
    problem = extracted_text
else:
    problem = st.text_area("Enter Problem",
                           "A ball is projected at 40 m/s at 45 degree")

# ==========================================================
# SMART PARSER
# ==========================================================
def extract(pattern, text):
    match = re.search(pattern, text.lower())
    return float(match.group(1)) if match else None

def classify(text):
    text = text.lower()
    if "degree" in text:
        return "Projectile"
    if "drop" in text:
        return "FreeFall"
    if "circular" in text:
        return "Circular"
    return "Vertical"

motion = classify(problem)

v = extract(r"(\d+)\s*m/s", problem) or 30
angle = extract(r"(\d+)\s*degree", problem) or 45
h = extract(r"(\d+)\s*m", problem) or 20

g = 9.8
dt = 0.02
time = np.arange(0, 30, dt)

# ==========================================================
# PHYSICS ENGINE (ALL MOTIONS REBUILT CLEAN)
# ==========================================================

x, y, z = [], [], []
vx_list, vy_list = [], []

max_time = 20

# ----------------------------------------
# PROJECTILE MOTION
# ----------------------------------------
if motion == "Projectile":

    vx = v * np.cos(np.radians(angle))
    vy = v * np.sin(np.radians(angle))
    vz = v * 0.25  # small depth for real 3D feel

    px, py, pz = 0, 0, 0

    t = 0
    while py >= 0 and t < max_time:

        x.append(px)
        y.append(py)
        z.append(pz)

        vx_list.append(vx)
        vy_list.append(vy)

        vy = vy - g * dt
        px = px + vx * dt
        py = py + vy * dt
        pz = pz + vz * dt

        t += dt

# ----------------------------------------
# VERTICAL THROW UP
# ----------------------------------------
elif motion == "Vertical":

    vy = v
    px = 0
    py = h
    pz = 0

    t = 0
    while py >= 0 and t < max_time:

        x.append(px)
        y.append(py)
        z.append(pz)

        vx_list.append(0)
        vy_list.append(vy)

        vy = vy - g * dt
        py = py + vy * dt

        t += dt

# ----------------------------------------
# FREE FALL
# ----------------------------------------
elif motion == "FreeFall":

    vy = 0
    px = 0
    py = h
    pz = 0

    t = 0
    while py >= 0 and t < max_time:

        x.append(px)
        y.append(py)
        z.append(pz)

        vx_list.append(0)
        vy_list.append(vy)

        vy = vy - g * dt
        py = py + vy * dt

        t += dt

# ----------------------------------------
# CIRCULAR MOTION
# ----------------------------------------
elif motion == "Circular":

    r = 10
    omega = v / r  # angular velocity

    t = 0
    while t < max_time:

        theta = omega * t

        px = r * np.cos(theta)
        py = r * np.sin(theta)
        pz = r * np.sin(theta/2)  # depth wave for 3D

        vx_val = -r * omega * np.sin(theta)
        vy_val = r * omega * np.cos(theta)

        x.append(px)
        y.append(py)
        z.append(pz)

        vx_list.append(vx_val)
        vy_list.append(vy_val)

        t += dt

# ----------------------------------------
# HORIZONTAL PROJECTION
# ----------------------------------------
elif "height" in problem.lower():

    vx = v
    vy = 0
    px = 0
    py = h
    pz = 0

    t = 0
    while py >= 0 and t < max_time:

        x.append(px)
        y.append(py)
        z.append(pz)

        vx_list.append(vx)
        vy_list.append(vy)

        vy = vy - g * dt
        px = px + vx * dt
        py = py + vy * dt

        t += dt

# ----------------------------------------
# SAFE FALLBACK
# ----------------------------------------
else:
    x = [0]
    y = [0]
    z = [0]
    vx_list = [0]
    vy_list = [0]

# Convert safely
x = np.array(x)
y = np.array(y)
z = np.array(z)
vx = np.array(vx_list)
vy = np.array(vy_list)



# ==========================================================
# ERROR ANALYSIS
# ==========================================================
st.markdown("### ⚠ Common Mistakes")

if motion == "Projectile":
    st.warning("Forgetting horizontal velocity is constant.")
    st.warning("Forgetting gravity acts only vertically.")

if motion == "Vertical":
    st.warning("Wrong sign of acceleration.")
    st.warning("Incorrect substitution in s = ut + ½at².")

# ==========================================================
# SELF TEST
# ==========================================================
st.markdown("### 📝 Test Yourself")

user_input = st.number_input("Enter Maximum Height:", value=0.0)

true_max = max(y) if len(y) > 0 else 0

if st.button("Check Answer"):
    st.session_state.attempts += 1
    if abs(user_input - true_max) < 2:
        st.success("Correct!")
        st.session_state.score += 1
    else:
        st.error(f"Incorrect. Correct ≈ {round(true_max,2)}")

# ==========================================================
# PERFORMANCE
# ==========================================================
st.markdown("### 📊 Performance Tracker")

st.write("Attempts:", st.session_state.attempts)
st.write("Correct:", st.session_state.score)

if st.session_state.attempts > 0:
    acc = (st.session_state.score / st.session_state.attempts) * 100
    st.write("Accuracy:", round(acc,2), "%")

# ==========================================================
# SIMULATION SECTION
# ==========================================================

if not mode_3d:

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line=dict(color="cyan", width=4),
        name="Trajectory"
    ))

    fig.add_trace(go.Scatter(
        x=[x[0]], y=[y[0]],
        mode="markers",
        marker=dict(size=14, color="red"),
        name="Object"
    ))

    if show_vectors and len(vx) > 0:
        fig.add_trace(go.Scatter(
            x=[x[0], x[0]+vx[0]*0.2],
            y=[y[0], y[0]+vy[0]*0.2],
            mode="lines",
            line=dict(color="yellow", width=5),
            name="Velocity"
        ))

    frames = []
    for i in range(len(x)):
        frames.append(go.Frame(
            data=[
                go.Scatter(x=x[:i+1], y=y[:i+1]),
                go.Scatter(x=[x[i]], y=[y[i]])
            ]
        ))

    fig.frames = frames

    fig.update_layout(
        template="plotly_dark",
        height=650,
        updatemenus=[{
            "type":"buttons",
            "bgcolor":"#111111",
            "bordercolor":"cyan",
            "font":{"color":"cyan","size":16},
            "buttons":[{
                "label":"▶ START SIMULATION",
                "method":"animate",
                "args":[None,{"frame":{"duration":15,"redraw":True}}]
            }]
        }]
    )

    st.plotly_chart(fig, width="stretch")

else:

    fig3d = go.Figure()

    fig3d.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode="lines",
        line=dict(color="cyan", width=6),
        name="3D Trajectory"
    ))

    fig3d.add_trace(go.Scatter3d(
        x=[x[0]], y=[y[0]], z=[z[0]],
        mode="markers",
        marker=dict(size=6, color="red"),
        name="Object"
    ))

    frames = []
    for i in range(len(x)):
        frames.append(go.Frame(
            data=[
                go.Scatter3d(x=x[:i+1], y=y[:i+1], z=z[:i+1]),
                go.Scatter3d(x=[x[i]], y=[y[i]], z=[z[i]])
            ]
        ))

    fig3d.frames = frames

    fig3d.update_layout(
        template="plotly_dark",
        height=750,
        scene=dict(
            xaxis_title="X Axis",
            yaxis_title="Height",
            zaxis_title="Depth",
            bgcolor="#0E1117",
            camera=dict(
                eye=dict(x=1.7, y=1.7, z=1.2)
            )
        ),
        updatemenus=[{
            "type":"buttons",
            "bgcolor":"#111111",
            "bordercolor":"cyan",
            "font":{"color":"cyan","size":16},
            "buttons":[{
                "label":"▶ START 3D SIMULATION",
                "method":"animate",
                "args":[None,{"frame":{"duration":15,"redraw":True}}]
            }]
        }]
    )

    st.plotly_chart(fig3d, width="stretch")
# ==========================================================
# ANALYSIS GRAPHS (RESTORED PROPERLY)
# ==========================================================

st.markdown("## 📊 Motion Analysis")

tabs = st.tabs(["Position vs Time",
                "Velocity vs Time",
                "Acceleration vs Time",
                "Energy Analysis"])

# Time axis
time_axis = np.linspace(0, len(x)*dt, len(x))

# ----------------------------------------
# POSITION GRAPH
# ----------------------------------------
with tabs[0]:
    fig_pos = go.Figure()

    fig_pos.add_trace(go.Scatter(
        x=time_axis,
        y=y,
        mode="lines",
        name="Height (Y)",
        line=dict(color="cyan", width=3)
    ))

    fig_pos.update_layout(
        template="plotly_dark",
        height=450,
        title="Position vs Time",
        xaxis_title="Time (s)",
        yaxis_title="Position"
    )

    st.plotly_chart(fig_pos, width="stretch")

# ----------------------------------------
# VELOCITY GRAPH
# ----------------------------------------
with tabs[1]:
    fig_vel = go.Figure()

    fig_vel.add_trace(go.Scatter(
        x=time_axis,
        y=vy,
        mode="lines",
        name="Velocity",
        line=dict(color="yellow", width=3)
    ))

    fig_vel.update_layout(
        template="plotly_dark",
        height=450,
        title="Velocity vs Time",
        xaxis_title="Time (s)",
        yaxis_title="Velocity"
    )

    st.plotly_chart(fig_vel, width="stretch")

# ----------------------------------------
# ACCELERATION GRAPH
# ----------------------------------------
with tabs[2]:
    acc_array = np.full(len(time_axis), -g)

    fig_acc = go.Figure()

    fig_acc.add_trace(go.Scatter(
        x=time_axis,
        y=acc_array,
        mode="lines",
        name="Acceleration",
        line=dict(color="red", width=3)
    ))

    fig_acc.update_layout(
        template="plotly_dark",
        height=450,
        title="Acceleration vs Time",
        xaxis_title="Time (s)",
        yaxis_title="Acceleration"
    )

    st.plotly_chart(fig_acc, width="stretch")

# ----------------------------------------
# ENERGY GRAPH
# ----------------------------------------
with tabs[3]:

    KE = 0.5 * (vx**2 + vy**2)
    PE = g * y
    Total_E = KE + PE

    fig_energy = go.Figure()

    fig_energy.add_trace(go.Scatter(
        x=time_axis,
        y=KE,
        mode="lines",
        name="Kinetic Energy",
        line=dict(color="orange", width=3)
    ))

    fig_energy.add_trace(go.Scatter(
        x=time_axis,
        y=PE,
        mode="lines",
        name="Potential Energy",
        line=dict(color="cyan", width=3)
    ))

    fig_energy.add_trace(go.Scatter(
        x=time_axis,
        y=Total_E,
        mode="lines",
        name="Total Energy",
        line=dict(color="green", width=3)
    ))

    fig_energy.update_layout(
        template="plotly_dark",
        height=450,
        title="Energy vs Time",
        xaxis_title="Time (s)",
        yaxis_title="Energy"
    )

    st.plotly_chart(fig_energy, width="stretch")
