intersection() {
        cylinder (h = 4, r=1, center = true, $fn=100);
        rotate ([90,0,0]) cylinder (h = 4, r=0.9, center = true, $fn=100);
}

//Union 并集 Difference 差集 intersection 交集