from shortcuts import r2r, json_response

def index(request):
    ctxt = {}
    ctxt['events'] = [
        dict(id=1, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=2, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=3, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=4, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=5, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=6, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=7, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=8, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=9, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=10, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=11, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=12, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=13, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=14, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
        dict(id=15, summary="dsh -Mcg nginx-www 'sudo kick'", progress=[1000, 500, 20],
             user="gary", tags=["kick", "dsh"], severity=3, start="2013-08-04 07:38:05", end="2013-08-04 07:38:05"),
    ]
    return r2r(request, "index", ctxt)
