def _16083420():
    result=[];
    course=input("你最喜欢的课程:");
    animal=input("你最喜欢的动物:");
    thing=input("大学最喜欢的事:");
    print("你最喜欢的课程:"+course);
    print("你最喜欢的动物:"+animal);
    print("大学最喜欢的事:"+thing);
    result.append(course)
    result.append(animal)
    result.append(thing)
    fpath = "D:\\result3.txt"
    with open(fpath, 'a', encoding='utf8') as f:
        for line in result:
            try:
                 f.write(str(line)+' ');

            except:
                print("写入出错")
                continue
if __name__ == "__main__":
    _16083420();