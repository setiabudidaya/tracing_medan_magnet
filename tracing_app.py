import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Define the magnetic field functions
def dipole(r0, theta_0, th):      # P(n=1, m=0)
    k = r0/(np.sin(theta_0)**2)
    return (k*np.sin(th)**2)

def quadpole(r0, theta_0, th):    # P(n=2, m=0)
    k = r0**2/(np.sin(theta_0)**2*np.cos(theta_0))
    P = np.cos(th)*np.sin(th)**2
    # Handle potential negative values before taking the square root
    return (np.sqrt(np.abs(k)*np.abs(P)))

def octpole(r0, theta_0, th):     # P(n=3, m=0)
    k = r0**3/(np.sin(theta_0)**2*(5*np.cos(theta_0)**2-1))
    P = (5*np.cos(th)**2-1)*np.sin(th)**2
    # Handle potential negative values before taking the cube root
    return ((np.abs(k)*np.abs(P))**(1/3))

def hexdpole(r0, theta_0, th):    # P(n=4, m=0)
    k = r0**4/((7*np.cos(theta_0)**3-3*np.cos(theta_0))*np.sin(theta_0)**2)
    P =(7*np.cos(th)**3-3*np.cos(th))*np.sin(th)**2
    # Handle potential negative values before taking the fourth root
    return ((np.abs(k)*np.abs(P))**(1/4))

# Create the Streamlit app interface
st.title("Tracing Magnetic Field Lines")

# Define the mapping from pole type number to name and function
names   = {1:'Dipole', 2:'Quadrupole', 3:'Octupole', 4:'Hexadecapole'}
axpoles = {1:dipole, 2:quadpole, 3:octpole, 4:hexdpole}

# Create the selectbox for pole type
pole_type_name = st.selectbox(
    "Pilih Tipe Kutub",
    options=list(names.values())
)

# Get the numerical pole_type based on the selected name
pole_type = list(names.keys())[list(names.values()).index(pole_type_name)]


# Create the text input for theta values
theta_input = st.text_input(
    "Masukkan Sudut Colatitude (derajat), dipisahkan koma",
    value="5, 10, 15, 20, 30, 40"
)

# Create the button to trigger plotting
plot_button = st.button("Buat Plot")

# Conditional block to generate the plot when the button is clicked
if plot_button:
    # Convert the comma-separated theta input string into a list of floats
    try:
        theta_list = [float(t.strip()) for t in theta_input.split(',') if t.strip()]
        # Basic validation for theta values
        if not all(0 <= t <= 90 for t in theta_list):
            st.error("Sudut colatitude harus antara 0 dan 90 derajat.")
            st.stop()
    except ValueError:
        st.error("Input theta values must be numbers separated by commas.")
        st.stop()

    # Proceed with plotting logic
    st.write(f"Generating plot for {names[pole_type]} field lines with starting colatitudes: {theta_list}")

    d2r     = np.deg2rad
    clines  = ['red', 'blue', 'grey', 'purple', 'brown', 'purple', 'pink', 'orange', 'magenta', 'olive', 'cyan']

    # Define the "Earth"
    r0  = 1
    the = d2r(np.linspace(0, 360, 1000))
    xe  = r0*np.sin(the)
    ye  = r0*np.cos(the)

    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_aspect('equal')
    ax.fill(xe, ye, color='lightgrey') # Plot the Earth

    ic = -1
    for i in theta_list:
        ic += 1
        theta_0 = d2r(i)
        # Ensure theta ranges from theta_0 to 90 degrees for plotting
        th = np.linspace(theta_0, d2r(90), 1000)
        rad = axpoles[pole_type](r0, theta_0, th)
        xb = rad*np.sin(th)
        yb = rad*np.cos(th)
        # Mask points inside the Earth (radius < 1)
        xb[np.where(rad<1)] = np.nan
        yb[np.where(rad<1)] = np.nan
        ax.plot(xb, yb, color = clines[ic%10])
        # Assume a symmetrical distribution in the four quadrants
        ax.plot( xb, -yb, color = clines[ic%10])
        ax.plot(-xb,  yb, color = clines[ic%10])
        ax.plot(-xb, -yb, color = clines[ic%10])


    ax.set_xlabel('Earth radii', fontsize=16)
    ax.set_ylabel('Earth radii', fontsize=16)
    ax.set_title(names[pole_type]+' field lines', fontsize=24);

    # Display the plot in Streamlit
    st.pyplot(fig)
