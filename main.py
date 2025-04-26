import numpy as np
import matplotlib.pyplot as plt

FreqReUse = 9
NoUpLink = 12
NtwSizeA=-2000
NtwSizeB=2000
PlusShift=12000
MinusShift=-12000
No_Iteration=1000

SDs = [4, 6, 10]
colors=['y', 'm', 'c']
labels=['SD=4', 'SD=6', 'SD=10']

for SDid, SD in enumerate(SDs):
    #[1][12] 크기의 빈 2차원 배열 생성
    SIR=np.zeros((1,NoUpLink))

    for Loop in range(0, No_Iteration):
        SubX = np.random.uniform(NtwSizeA, NtwSizeB, size=[FreqReUse, NoUpLink])
        SubY = np.random.uniform(NtwSizeA, NtwSizeB, size=[FreqReUse, NoUpLink])

        Cell_x0 =  SubX[0, :]
        Cell_y0 = SubY[0, :]
        Cell_x1 = SubX[1, :]
        Cell_y1 = SubY[1, :] + PlusShift
        Cell_x2 = SubX[2, :] + PlusShift
        Cell_y2 = SubY[2, :] + PlusShift
        Cell_x3 = SubX[3, :] + PlusShift
        Cell_y3 = SubY[3, :]
        Cell_x4 = SubX[4, :] + PlusShift
        Cell_y4 = SubY[4, :] + MinusShift
        Cell_x5 = SubX[5, :]
        Cell_y5 = SubY[5, :] + MinusShift
        Cell_x6 = SubX[6, :] + MinusShift
        Cell_y6 = SubY[6, :] + MinusShift
        Cell_x7 = SubX[7, :] + MinusShift
        Cell_y7 = SubY[7, :]
        Cell_x8 = SubX[8, :] + MinusShift
        Cell_y8 = SubY[8, :] + PlusShift

        ShiftX = np.array([Cell_x0, Cell_x1, Cell_x2, Cell_x3, Cell_x4, Cell_x5, Cell_x6, Cell_x7, Cell_x8])
        ShiftY = np.array([Cell_y0, Cell_y1, Cell_y2, Cell_y3, Cell_y4, Cell_y5, Cell_y6, Cell_y7, Cell_y8])

        #[0,0] 위치에서부터 각 NoUpLink의 거리를 계산
        Dist = np.sqrt(ShiftX**2+ShiftY**2)

        #각 FreqReUSe의 NoUpLink마다 랜덤으로 Power를 모델링함. 보강/상세간섭을 예상해서 NormalDistribution으로 0을 중심으로 -6~6까지 사이의 값들이 총 68%를 차지함
        NormalDistribution = np.random.randn(FreqReUse, NoUpLink)
        mu = 0
        LogNormal = mu + SD*NormalDistribution

        #각 FreqReUse의 NoUpLink마다 Power(보강간섭/상세간섭 영향 포함)에서 Distance를 감안한 Power 값 생성
        LogNormalP = 10**(LogNormal/10)/(Dist**4)

        PS = LogNormalP[0, :]
        PI1 = LogNormalP[1, :]
        PI2 = LogNormalP[2, :]
        PI3 = LogNormalP[3, :]
        PI4 = LogNormalP[4, :]
        PI5 = LogNormalP[5, :]
        PI6 = LogNormalP[6, :]
        PI7 = LogNormalP[7, :]
        PI8 = LogNormalP[8, :]

        #각 station들의 NoUpLink들의 값을 합쳐서 1차원 배열
        PI = PI1 + PI2 + PI3 + PI4 + PI5 + PI6 + PI7 + PI8
        #PS(Base Station)의 NoUpLink들을 기준으로 타 station들의 NoUpLink들이 느끼는 SIR을 계산
        SIRn = PS/PI

        SIRdB = 10*np.log10(SIRn)
        
        #행 추가
        SIR = np.vstack((SIR, SIRdB))
    #SIR의 첫번째 행 (SIR = np.zeros(1, NoUpLink))으로 더해진 [0,0,0,0,0,0,0,0,...] 행 삭제
    SIR=np.delete(SIR, 0, 0)
    SIR = SIR.flatten()

