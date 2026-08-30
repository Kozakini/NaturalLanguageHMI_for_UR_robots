import rtde_receive
import rtde_control

ctrl = rtde_control.RTDEControlInterface("127.0.0.1")
recv = rtde_receive.RTDEReceiveInterface("127.0.0.1")

# Sprawdź aktualną pozycję
pose = recv.getActualTCPPose()
print(f"Pozycja TCP: {pose}")

# Prosty ruch — moveJ (ruch po osiach)
# [base, shoulder, elbow, wrist1, wrist2, wrist3] w radianach
ctrl.moveJ([0, -1.57, 0, -1.57, 0, 0], speed=0.5, acceleration=0.3)
print("Ruch wykonany!")
