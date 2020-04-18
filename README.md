# hate-speech-language-modeling
Recurrent Neural Network based Hate Speech Language Model for Korean Hate Speech Detection 
<br>- by Yoo Byoung Woo  

web service available (try it yourself!!!): https://hate-speech-main-c2eedpqzcq-an.a.run.app
<br>demo video: https://www.youtube.com/watch?v=HnhS6BgmcDg
<br>the models and datasets are available at https://www.kaggle.com/captainnemo9292/korean-hate-speech-dataset

안녕하세요 Github, 딥러닝에 관심있는 고등학생입니다. 이번에 발생한 n번방 사태에 대해 큰 충격을 받고, 우리나라의 혐오 문화를 AI로 접근할 방법이 있을까 생각하다가 인공지능 기반 혐오 발언 탐지 웹서비스를 구현해보았습니다. 극우 사이트 일간베스트의 댓글들을 학습 데이터로써 크롤링하여 혐오 발언 이진 분류 RNN 모델을 개발했고, NMF 토픽 모델 알고리즘을 활용하여 혐오 발언의 주제를 추출하여 multi-class classification 언어 모델을 학습시켰습니다. ( 주제 1 - 특정 지역에 대한 차별, 주제 2 - 정치적 성향이 다른 사람들에 대한 왜곡, 주제 3 - 다른 나라에 대한 차별, 주제 4 - 여성 차별 및 성적 발언) 한 번씩 봐주시면 감사하겠습니다.

p.s.본래 BERT에다 전이 학습 시켜서 성능이 훨씬 좋았는데, 메모리를 너무 많이 잡아먹어 웹 서비스가 다운된다는 문제게 생기기 때문에 간단한 RNN으로 대체했습니다. 따라서 성능이 좋지 않다고 보실 수도 있습니다. 제가 전문가가 아니라는 점 가만해 주십시오
