변경한 파일 : SimpleScene
            - def CatmullRomSpline(p0,p1,p2,p3,t): t에 따라 CatmullRomSpline에서의 위치을 반환하는 함수
            - 마우스 클릭 부분에서 소를 클릭하고 6번까지는 클릭마다, 소가 복사되고, 누른상태로 움직이면 수직이동이 가능하도록 제작
            -  display함수 내에서 6개의 점을 지나는 CatmullRomSpline을 따라, 소의 위치가 이동되고, 이전프레임의 위치와 현재프레임의 위치에 따라
            소가 바라 보는 방향을 변경함 