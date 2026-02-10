"""resume_v1.doc 채움 결과 검증 (win32com)"""
import os
import sys
import io
import win32com.client

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DOC_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'drafts', 'resume_v1.doc')
)


def verify(doc_path):
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = False

    try:
        doc = word.Documents.Open(doc_path, ReadOnly=True)

        checks = []

        # Table 1: 지원분야
        t1 = doc.Tables(1)
        company = t1.Cell(1, 3).Range.Text.strip().replace('\r', '').replace('\x07', '')
        position = t1.Cell(2, 3).Range.Text.strip().replace('\r', '').replace('\x07', '')
        checks.append(('지원분야-회사', company, bool(company)))
        checks.append(('지원분야-직무', position, bool(position)))

        # Table 3: 인적사항
        t3 = doc.Tables(3)
        name_ko = t3.Cell(1, 4).Range.Text.strip().replace('\r', '').replace('\x07', '')
        birth = t3.Cell(1, 6).Range.Text.strip().replace('\r', '').replace('\x07', '')
        name_en = t3.Cell(2, 4).Range.Text.strip().replace('\r', '').replace('\x07', '')
        address = t3.Cell(3, 3).Range.Text.strip().replace('\r', '').replace('\x07', '')
        email = t3.Cell(4, 3).Range.Text.strip().replace('\r', '').replace('\x07', '')
        phone = t3.Cell(5, 5).Range.Text.strip().replace('\r', '').replace('\x07', '')
        checks.append(('이름(한)', name_ko, '임종권' in name_ko))
        checks.append(('생년월일', birth, '1992' in birth))
        checks.append(('이름(영)', name_en, 'Lim' in name_en))
        checks.append(('주소', address[:30], bool(address)))
        checks.append(('이메일', email, '@' in email))
        checks.append(('휴대폰', phone, '010' in phone))

        # Table 4: 학력
        t4 = doc.Tables(4)
        hs = t4.Cell(2, 2).Range.Text.strip().replace('\r', '').replace('\x07', '')
        univ = t4.Cell(4, 2).Range.Text.strip().replace('\r', '').replace('\x07', '')
        grad = t4.Cell(5, 2).Range.Text.strip().replace('\r', '').replace('\x07', '')
        checks.append(('고등학교', hs, bool(hs)))
        checks.append(('대학교', univ, '숭실' in univ))
        checks.append(('대학원', grad, '숭실' in grad or '사회복지' in grad))

        # Table 5: 경력
        t5 = doc.Tables(5)
        c1 = t5.Cell(2, 2).Range.Text.strip().replace('\r', '').replace('\x07', '')
        c2 = t5.Cell(3, 2).Range.Text.strip().replace('\r', '').replace('\x07', '')
        c3 = t5.Cell(4, 2).Range.Text.strip().replace('\r', '').replace('\x07', '')
        checks.append(('경력1', c1, '함께만드는세상' in c1))
        checks.append(('경력2', c2, '맨지온' in c2))
        checks.append(('경력3', c3, '엣지크로스' in c3))

        # Table 6: 자격증
        t6 = doc.Tables(6)
        cert1 = t6.Cell(2, 2).Range.Text.strip().replace('\r', '').replace('\x07', '')
        cert2 = t6.Cell(2, 5).Range.Text.strip().replace('\r', '').replace('\x07', '')
        checks.append(('자격증1', cert1, '사회복지사' in cert1))
        checks.append(('자격증2', cert2, '운전면허' in cert2))

        # Table 7: 기타
        t7 = doc.Tables(7)
        mil = t7.Cell(2, 6).Range.Text.strip().replace('\r', '').replace('\x07', '')
        checks.append(('병역-군별', mil, '공군' in mil))

        # Table 8: 자기소개서
        t8 = doc.Tables(8)
        intro1 = t8.Cell(2, 1).Range.Text.strip().replace('\r', '').replace('\x07', '')
        intro2 = t8.Cell(4, 1).Range.Text.strip().replace('\r', '').replace('\x07', '')
        intro3 = t8.Cell(6, 1).Range.Text.strip().replace('\r', '').replace('\x07', '')
        checks.append(('성격소개', intro1[:40] + '...', len(intro1) > 50))
        checks.append(('경력특기', intro2[:40] + '...', len(intro2) > 50))
        checks.append(('지원동기', intro3[:40] + '...', len(intro3) > 50))

        # 결과 출력
        print("=" * 60)
        print("VERIFICATION RESULT")
        print("=" * 60)
        all_pass = True
        for label, value, ok in checks:
            status = "✅" if ok else "❌"
            if not ok:
                all_pass = False
            print(f"  {status} {label}: {value}")

        print()
        if all_pass:
            print("🎉 ALL CHECKS PASSED")
        else:
            print("⚠️ SOME CHECKS FAILED — review above")

        # 페이지 수 확인
        pages = doc.ComputeStatistics(2)  # wdStatisticPages
        print(f"\n📄 Total pages: {pages}")

        doc.Close(False)
    finally:
        word.Quit()


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else DOC_PATH
    verify(path)
