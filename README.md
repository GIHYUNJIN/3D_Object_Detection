 # pointpillars-lidar_road

본 레포지토리는 Lidar 센서를 이용한 3차원 객체 탐지에 특화된 Pointpillars 모델의 학습 및 추론 코드를 제공합니다.
원본 코드는 [pointpillars](https://github.com/open-mmlab/OpenPCDet?tab=readme-ov-file)임을 밝힙니다.

official code for the paper : https://arxiv.org/abs/1812.05784


## 모델 정보

PointPillars는 point cloud를 bev (bird’s-eye view)를 기준으로 구역화하여 pillars를 만들고, 해당 pillars를 pillar feature net이 입력받아 detection의 CNN 네트워크를 사용하기에 적절한 pseudo-image를 만듭니다. 이후 CNN 기반 backbone 네트워크와 detection head를 통해 물체를 탐지하고 3D bbox를 결정합니다.

![PointPillar 구조](docs/pointpillars.png)

## Dependencies
- Python 3.10.10
- PyTorch 2.0.0
- CUDA 11.7


## 1. conda 가상환경 생성
```
cd /root/pointpillars-lidar_road/OpenPCDet/
conda env create -f conda_requirements.yaml
conda init
source ~/.bashrc
conda activate openpc
```

## 2. 학습 데이터 준비
- /root/data/ 폴더 안에 36_3, 36_4, 36_5 폴더 생성
   - 36_3 : 주간
   - 36_4 : 야간
   - 36_5 : 악천후
- 각 폴더(36_3, 36_4, 36_5) 내부에 json, labels, pcd, points 폴더 생성
- .json(레이블 정보) 파일과 .pcd(point cloud data)를 json, pcd 파일에 업로드

## 3. 전처리
#### 3-1. 데이터 포맷 변환
- json, txt 파일을 pcd, npy 형태로 변환
```
cd /root/pointpillars-lidar_road/OpenPCDet/
python convert.py --path {}
```
- path : 변환할 데이터 경로
    - /root/data/36_3 : 주간
    - /root/data/36_4 : 야간
    - /root/data/36_5 : 악천후

#### 3-2. 데이터 분할
```
python split.py --path {}
```
- path : 분할할할 데이터 경로
    - /root/data/36_3 : 주간
    - /root/data/36_4 : 야간
    - /root/data/36_5 : 악천후

#### 3-3. dbinfo 파일 생성
```
cd /root/pointpillars-lidar_road/OpenPCDet/tools/
python -m pcdet.datasets.custom.custom_dataset create_custom_infos {config_file_path}
```
- config_file_path : dbinfo 파일을 생성하기 위한 config 파일 경로
    - cfgs/dataset_configs/custom_dataset_3.yaml  : 주간
    - cfgs/dataset_configs/custom_dataset_4.yaml  : 야간
    - cfgs/dataset_configs/custom_dataset_5.yaml  : 악천후

## 4. 학습
```
cd /root/pointpillars-lidar_road/OpenPCDet/tools/
python train.py --cfg_file {config_file_path} --epochs {epoch} --batch_size {batch_size} --extra_tag {tag}
# example
python train.py --cfg_file cfgs/custom_models/pointpillar_custom_3.yaml --epochs 100 --batch_size 32 --extra_tag 36_3
```
- config_file_path : 학습을 위한 config 파일 경로
- epoch : epoch 수 지정
- batch_size : batch 크기 지정
- extra_tag : tag 지정


## 5. 추론
```
python test.py --cfg_file {config_file_path} --batch_size {batch_size} --ckpt {checkpoint_file_path} --file_name {file_name}
# example
python test.py --cfg_file cfgs/custom_models/pointpillar_custom_3.yaml --batch_size 32 --ckpt ../output/custom_models/pointpillar_custom_3/36_3/ckpt/checkpoint_epoch_150.pth --file_name 16_113821_220609_31
```
- config_file_path : 추론을 위한 config 파일 경로
- batch_size : batch 크기 지정
- checkpoint_file_path : 학습된 파일 경로
- file_name : 추론할 파일 ID
    - 1개의 파일을 추론하고 싶으면 이 argument 를 지정해서 사용


## 6. 추론 결과
```
{'name': array(['vehicle'], dtype='<U11'), 'score': array([0.6290256], dtype=float32), 'boxes_lidar': array([[46.773735  ,  0.16365868,  0.7637941 ,  3.3010871 ,  2.1215076 ,
         1.0947162 ,  6.293104  ]], dtype=float32), 'pred_labels': array([1]), 'frame_id': '16_113821_220609_31'}
```
- 탐지한 객체 이름(name), 3차원 공간상의 좌표(boxes_lidar)가 추론 됨

## 7. 데모
```
cd /root/pointpillars-lidar_road/OpenPCDet/demo
python app.py
```
- point cloud data(.npy)를 업로드 하면 탐지한 객체가 3차원으로 시각화 됨

<img src="docs/demo_screenshot_0.png" width=700>
<img src="docs/demo_screenshot_1.png" width=700>

## LICEAN
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
