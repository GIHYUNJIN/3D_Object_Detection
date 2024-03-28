import open3d
import plotly.graph_objects as go
import numpy as np
import matplotlib.cm as cm

# 각 객체에 대한 색상 매핑
box_colormap  = {
    'vehicle': [0, 1, 0],        # 차량: 녹색
    'bus': [1, 0, 0],            # 버스: 빨강
    'truck': [0, 0, 1],          # 트럭: 파랑
    'policecar': [1, 1, 0],      # 경찰차: 노랑
    'ambulance': [1, 0.5, 0],    # 구급차: 주황
    'schoolbus': [0.5, 0, 0.5],  # 스쿨버스: 보라
    'othercar': [0, 0.5, 0.5],   # 기타 차량: 청록
    'trafficsign': [0.5, 0.5, 0.5]  # 교통 신호: 회색
}

def draw_scenes(points, gt_boxes=None, ref_boxes=None, ref_labels=None, ref_scores=None, point_colors=None, draw_origin=True):
    fig = go.Figure()
    points = points.cpu().numpy()

    # Draw points
    if point_colors is None:
        point_colors = np.ones((points.shape[0], 3))  # Default color: white
    point_trace = go.Scatter3d(
        x=points[:, 0], y=points[:, 1], z=points[:, 2],
        mode='markers',
        marker=dict(
            size=1,  # Adjust point size as needed
            color=point_colors,
            opacity=1
        ),
        name='Points'
    )
    fig.add_trace(point_trace)

    # Draw origin
    if draw_origin:
        axis_length = 1.0
        origin_trace = go.Scatter3d(
            x=[0, axis_length, 0, 0, 0],
            y=[0, 0, axis_length, 0, 0],
            z=[0, 0, 0, axis_length, 0],
            mode='lines',
            line=dict(color='black', width=4),
            name='Origin'
        )
        fig.add_trace(origin_trace)

    # Draw boxes
    if gt_boxes is not None:
        for i in range(gt_boxes.shape[0]):
            line_set, _ = translate_boxes_to_open3d_instance(gt_boxes[i])
            box_trace = line_set_to_plotly_mesh3d(line_set, color=(0, 0, 1), name='gt_box_' + str(i))
            fig.add_trace(box_trace)

    if ref_boxes is not None:
        ref_boxes = ref_boxes.cpu().numpy()
        ref_labels = ref_labels.cpu().numpy()  # CPU로 이동
        for i in range(ref_boxes.shape[0]):
            line_set, _ = translate_boxes_to_open3d_instance(ref_boxes[i])
            box_colormap_keys = list(box_colormap.keys())
            label = box_colormap_keys[ref_labels[i]-1]
            color = box_colormap[label] if label in box_colormap else (1, 0, 0)  # 지정된 레이블이 없을 경우 빨간색
            color = np.clip(color, 0, 1)  # 색상 값을 [0, 1] 범위 내로 클리핑
            box_trace = line_set_to_plotly_mesh3d(line_set, color=color)
            box_trace.name = str(label)  # 객체의 이름을 문자열로 설정
            fig.add_trace(box_trace)

    # 범례 추가
    fig.update_layout(
        legend=dict(
            title='Labels',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    # Update layout
    fig.update_layout(
        scene=dict(
            aspectmode='data',
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Z')
        )
    )

    return fig

def translate_boxes_to_open3d_instance(gt_boxes):
    center = gt_boxes[0:3]
    lwh = gt_boxes[3:6]
    axis_angles = np.array([0, 0, gt_boxes[6] + 1e-10])
    rot = open3d.geometry.get_rotation_matrix_from_axis_angle(axis_angles)
    box3d = open3d.geometry.OrientedBoundingBox(center, rot, lwh)

    line_set = open3d.geometry.LineSet.create_from_oriented_bounding_box(box3d)

    lines = np.asarray(line_set.lines)
    lines = np.concatenate([lines, np.array([[1, 4], [7, 6]])], axis=0)
    line_set.lines = open3d.utility.Vector2iVector(lines)

    return line_set, box3d


# RGB 값인 color를 색상 문자열로 변환
def rgb_to_plotly_color(rgb):
    return 'rgb({}, {}, {})'.format(*rgb)

def line_set_to_plotly_mesh3d(line_set, color):
    lines = np.asarray(line_set.lines)
    points = np.asarray(line_set.points)
    x_lines = points[lines[:, 0], 0]
    y_lines = points[lines[:, 0], 1]
    z_lines = points[lines[:, 0], 2]

    # Normalize color values to range [0, 1]
    color = np.clip(color, 0, 1)  # Ensure color values are within [0, 1]

    mesh_trace = go.Mesh3d(
        x=x_lines,
        y=y_lines,
        z=z_lines,
        i=lines[:, 0],
        j=lines[:, 1],
        k=np.zeros_like(lines[:, 0]),
        color='rgb({}, {}, {})'.format(int(color[0]*255), int(color[1]*255), int(color[2]*255)),  # Convert color to RGB string
        opacity=0.5,
        name='Box'
    )

    return mesh_trace
