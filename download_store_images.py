"""
가게 이미지를 직접 다운로드해서 static 폴더에 저장하는 스크립트.

사용법:
    1. 이 파일을 Hackathon_3 프로젝트 루트(manage.py가 있는 위치)에 복사
    2. (venv 활성화 상태에서) 아래 명령 실행
         python download_store_images.py
    3. deliverys/static/deliverys/images/stores/ 폴더에 24개 이미지가 저장됨

※ 이 스크립트는 사용자 컴퓨터에서 직접 실행해야 함
   (Claude의 작업 환경은 외부 네트워크 접근이 제한돼 있어서 이 다운로드를 대신 실행할 수 없음)
"""
import os
import io
import urllib.request

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Pillow이 없어서 원본 확장자 그대로 저장합니다. (pip install Pillow 하면 전부 .jpg로 통일됩니다)")

STORES = [
    ("dongdaemun_yeopgi_tteokbokki", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMjA0MDJfNDkg%2FMDAxNjQ4ODY3OTU2NDM2.QYrmT95DrVgSuly-dmRcmktUncf-U0v0sRMgMjyqv5sg.BTbS5JWr46IfciX4ivstoYcF7tjiU5mEvTXKiPSDuJ8g.PNG.tlstnqls0719%2Fimage%25A3%25A5EF%25A3%25A5BC%25A3%25A585EF%25A3%25A5EF%25A3%25A5BC%25A3%25A585BC%25A3%25A5EF%25A3%25A5BC%25A3%25A5858D1%25A3%25A5EF%25A3%25A5BC%25A3%25A585EF%25A3%25A5EF%25A3%25A5BC%25A3%25A585BC%25A3%25A5EF%25A3%25A5BC%25A3%25A5858Dremo.png&type=a340"),
    ("eunggeupsil_gukmul_tteokbokki", "https://search.pstatic.net/sunny/?src=https%3A%2F%2Ffile.albamon.com%2FAlbamon%2FRecruit%2FPhoto%2FC-Photo-View%3FFN%3D2023%2F10%2F18%2FJK_CO_ordnwj23101811220964.jpg&type=a340"),
    ("ssada_gimbap", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA5MTdfMjc3%2FMDAxNjMxODEzMzQ3NzAx.nK5A9xXIPyHAXbdA4HiYJvgAMBQ7tKhWMNcAUJDQIfMg.0CtkGVCp9l6RUZQ0jGw2WV4waYaQndwgEqjU12R91y8g.PNG.write90%2Fimage.png&type=a340"),
    ("schoolfood_delivery", "https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F5612%2F2018%2F12%2F31%2F0000003589_001_20181231150209821.jpg&type=a340"),
    ("syangcheu_mala", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNDA3MjlfMjE5%2FMDAxNzIyMTc5MTcyMDM2.tUzxvTpcCFSbB4P6GojGKbNsy-z9M-uRPqmS1CsVcukg.8lk1m6p-R2aabSLguUovs5RtzQ6PG_gVdC9mMvS_PCIg.JPEG%2FIMG_1968.jpg&type=a340"),
    ("hongkong_banjeom", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxODA5MTdfMjMz%2FMDAxNTM3MTUzNDgyNDU0.H3eJQ5VRxHRZmEiz3clVr8wZ5ebw_bJKZXwx-XRZ210g.Cq-P5Yz6YCwQNn7tfQv5C9EUzp5rxT0ZcJuJi21Qhgwg.PNG.mkg_suwon%2F1526310256285_icon.png&type=a340"),
    ("chunli_malatang", "https://search.pstatic.net/common/?src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20210527_229%2F1622119587759T9BH6_JPEG%2FE3DimFBPxC9IAoEa-i3Dz0zw.jpg&type=a340"),
    ("piro_banjeom", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNjAxMTFfMjEw%2FMDAxNzY4MTA0MjM2NzA2.yy9ObHkY-JmclOxyaCKrGalZtzGpti4n38Fg2EeoR4kg.RPxmLgwsvcxRMHcEVicNedZzdMdYCoaPc6uwVhtaCVog.JPEG%2Fgen_1768104175_1_9167.jpg&type=a340"),
    ("pildong_jokbal", "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fimage.utoimage.com%2Fpreview%2Fcp871385%2F2018%2F12%2F201812006026_500.jpg&type=a340"),
    ("mawang_jokbal", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDA1MTJfMTc0%2FMDAxNTg5MjY4MDAzMDUw.oXWjTwyyzdUL08UEoeOvTxuQosiFLMARugsFkj-0cTIg.zlpoLoFK3vbyFZ7wjxlcXabWsK43KkYwzF06J7qRY28g.JPEG.gudwnslaaa%2F111.jpg&type=a340"),
    ("wonhalmeoni_bossam_jokbal", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxODAzMTdfMTg1%2FMDAxNTIxMjU3NTQyNjIy.hWedEryCnB3iwmxcQSG4-t3FI9M8TtvGCgRjgaorBM4g.Dc60BKN6pxH6A7jCa9BXPHBzRwcVkZi0w2rlVjPM8YEg.PNG.rrd753%2F20180317_115229.png&type=a340"),
    ("piro_jokbal", "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fthumb2.gettyimageskorea.com%2Fimage_preview%2F700%2F201711%2FMBRF%2FMBRF17017941.jpg&type=a340"),
    ("mcdonalds", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxODA2MTFfMTIx%2FMDAxNTI4NzAyNTQwMTcy.uGwJ0VME93FnIOu8TMtYodB5SL7r936q5mFHe4obdmgg.H8ZHqFCRj5BLKdDNx4ICaghnU7_aU722WpW2qpJEWrIg.JPEG.thenemolab%2F%25B8%25C6%25B5%25B5%25B3%25AF%25B5%25E52018.jpg&type=a340"),
    ("lotteria", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2F20140506_37%2Fcheapburger_13993863873401cmr0_PNG%2FB7%253FA5B8AEBEC6_BCBCB7CEC7FC_red.png&type=a340"),
    ("burgerking", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNTA0MzBfMjE5%2FMDAxNzQ2MDE1NjU0ODgx.qzhAJ2VyLavjwgrdFc4pZizZA1eZZWd-9L4nBgf1bvUg.PLTQpNanVV-QmShD7VypjW_w-0myuXf10xqtI_xKh_0g.JPEG%2F%25B9%25F6%25B0%25C5%25C5%25B7%25B7%25CE%25B0%25ED.jpg&type=a340"),
    ("momstouch", "https://search.pstatic.net/sunny/?src=https%3A%2F%2Ft1.daumcdn.net%2Fcafeattach%2F1IHuH%2F857c123390f073525a870f48c8b5c2fd6be67633&type=a340"),
    ("mega_mgc_coffee", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMjA4MzBfMTMw%2FMDAxNjYxODMzNDg1MTg5.mMm-TihJp_csGsgvk-TzU6KkBGQjzYK9By3Gbqd7qQcg.XplQ7wUaYKb2yv5FnI4jZcQVLELvhazs_znUThcR-7og.PNG.po00206%2Fbi_logo1.png&type=l340_165"),
    ("twosome_place", "https://search.pstatic.net/sunny/?src=https%3A%2F%2Fi.pinimg.com%2F736x%2Ff8%2Fef%2F91%2Ff8ef915154fe8b822b451aea4a7a8e48.jpg&type=a340"),
    ("dunkin", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAxOTA4MDFfMzgg%2FMDAxNTY0NjQ1OTAzMjMz.SbUOz-VXJlS37BNTTFw1fTTuIEUDJA6o9iJbpOq4wMUg.NVxuAMl9ZxwhmEeqpdRe_h9pMDHhPB69NIgTNH4m4Zkg.JPEG.duckdesign%2F0cHLGe6M_400x400.jpg&type=a340"),
    ("compose_coffee", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNTA5MjVfNCAg%2FMDAxNzU4Nzc2MTI4MjM0.MWQHWzzVUtOWVH1EnLQ7h4xJ1sp5BAxSmK--t3yllQcg.L64Dnhspxm8ozjiMgG0EvcGU-00AGs1wE-MiF-tacEcg.PNG%2F%25B4%25D9%25BF%25EE%25B7%25CE%25B5%25E5_%25281%2529.png&type=a340"),
    ("kyochon", "https://search.pstatic.net/common/?src=http%3A%2F%2Fimgnews.naver.net%2Fimage%2F5562%2F2020%2F08%2F14%2F0000012854_001_20200814102054160.jpg&type=a340"),
    ("bhc", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMTA2MTZfMjg3%2FMDAxNjIzODA2NDc3NjY5.ooK9MfX81XTOznDbUiJCgeg5zl30JbOAJtypG0id_zMg.TR1JrvWOQQXvTWdNrYriizVaP0PovnTy2sIsoXfw-mgg.JPEG.congha%2Fbhc1.jpg&type=a340"),
    ("bbq", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMzEyMTVfMjE1%2FMDAxNzAyNjE2NDQ4MzMy.IMCFZgy0hrz0r6kLG2c8yEkCJtbK7wJyTNMcBVbyTiog.Zgxr85up_ouZX9T1hvT8qngh0sB4IG6E1pfjKG2ra9Ig.PNG.moneyhero7779%2Fimage.png&type=a340"),
    ("goobne_chicken", "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyMDExMTZfMjc5%2FMDAxNjA1NDg0MzU0MDM5.SiiTJ_-VMrrdUdOQIkyn9RfAblNai0oxIKNbuD6Dpvcg.7vFXLFcesuPJVaE3vznJ7BAwE6-9Sihqry36bmy9myQg.PNG.ryowoo48%2F%25BD%25BA%25C5%25A9%25B8%25B0%25BC%25A6_2020-11-16_%25BF%25C0%25C0%25FC_8.51.52.png&type=a340"),
]

OUT_DIR = os.path.join("deliverys", "static", "deliverys", "images", "stores")

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for slug, url in STORES:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = resp.read()

            if HAS_PIL:
                # 확장자를 전부 .jpg로 통일 (views.py에서 항상 <slug>.jpg로 참조하기 위함)
                img = Image.open(io.BytesIO(data)).convert("RGB")
                out_path = os.path.join(OUT_DIR, f"{slug}.jpg")
                img.save(out_path, "JPEG", quality=90)
                print(f"OK   {slug}.jpg  ({len(data)} bytes -> converted)")
            else:
                ctype = resp.headers.get("Content-Type", "")
                ext = "png" if "png" in ctype else ("gif" if "gif" in ctype else "jpg")
                out_path = os.path.join(OUT_DIR, f"{slug}.{ext}")
                with open(out_path, "wb") as f:
                    f.write(data)
                print(f"OK   {slug}.{ext}  ({len(data)} bytes, 원본 형식 그대로)")
        except Exception as e:
            print(f"FAIL {slug}: {e}")

if __name__ == "__main__":
    main()