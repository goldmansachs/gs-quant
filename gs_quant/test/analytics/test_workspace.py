"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

import pytest

from gs_quant.analytics.workspaces import PlotComponent, WorkspaceRow, Workspace, WorkspaceColumn


def test_layout_creation():
    plot_component_1 = PlotComponent(200, id_='CHCHF6NW1KXKFDAG')
    plot_component_2 = PlotComponent(200, id_='CHCHF6NW1KXKFDAG')
    plot_component_3 = PlotComponent(550, id_='CHCHF6NW1KXKFDAG')
    plot_component_4 = PlotComponent(550, id_='CHCHF6NW1KXKFDAG', width=8)

    # Case 1: Simple layout
    rows = [
        WorkspaceRow(components=[plot_component_1, plot_component_2])
    ]
    workspace = Workspace(rows=rows, alias='testing-something', name='Testing')
    workspace = workspace.as_dict()
    assert workspace['parameters']['layout'] == 'r(c6($0)c6($1))'

    # Case 2: Extra columns equal spaced layout
    rows = [
        WorkspaceRow(components=[
            WorkspaceColumn(components=[WorkspaceRow(components=[plot_component_1]),
                                        WorkspaceRow(components=[plot_component_2])]),
            plot_component_3
        ])
    ]
    workspace = Workspace(rows=rows, alias='testing-something', name='Testing')
    workspace = workspace.as_dict()
    assert workspace['parameters']['layout'] == 'r(c6(r(c12($0))r(c12($1)))c6($2))'

    # Case 3: Simple non-equal layout
    rows = [
        WorkspaceRow(components=[plot_component_4, plot_component_2])
    ]
    workspace = Workspace(rows=rows, alias='testing-something', name='Testing')
    workspace = workspace.as_dict()
    assert workspace['parameters']['layout'] == 'r(c8($0)c4($1))'

    # Case 4: Non-equal spacing
    rows = [
        WorkspaceRow(components=[
            WorkspaceColumn(width=8, components=[WorkspaceRow(components=[plot_component_1]),
                                                 WorkspaceRow(components=[plot_component_2])]),
            plot_component_3
        ])
    ]
    workspace = Workspace(rows=rows, alias='testing-something', name='Testing')
    workspace = workspace.as_dict()
    assert workspace['parameters']['layout'] == 'r(c8(r(c12($0))r(c12($1)))c4($2))'


def test_layout_parsing():
    plot_component_1 = PlotComponent(1, id_='CHCHF6NW1KXKFDAG')  # 0 is not supported for height
    plot_component_2 = PlotComponent(2, id_='CHCHF6NW1KXKFDAG')
    plot_component_3 = PlotComponent(3, id_='CHCHF6NW1KXKFDAG')

    # Case 1: Single Component
    rows = [
        WorkspaceRow(components=[plot_component_1])
    ]
    workspace = Workspace(rows=rows, alias='testing-something', name='Testing')
    workspace = Workspace.from_dict(workspace.as_dict())

    assert isinstance(workspace.rows[0], WorkspaceRow)
    assert isinstance(workspace.rows[0].components[0], PlotComponent)
    assert workspace.rows[0].components[0].width == 12
    assert workspace.rows[0].components[0].height == 1

    # Case 2: 2 Components
    rows = [
        WorkspaceRow(components=[plot_component_1, plot_component_2])
    ]
    workspace = Workspace(rows=rows, alias='testing-something', name='Testing')
    workspace = Workspace.from_dict(workspace.as_dict())

    assert isinstance(workspace.rows[0], WorkspaceRow)
    assert isinstance(workspace.rows[0].components[0], PlotComponent)
    assert workspace.rows[0].components[0].width == 6
    assert workspace.rows[0].components[0].height == 1
    assert isinstance(workspace.rows[0], WorkspaceRow)
    assert isinstance(workspace.rows[0].components[1], PlotComponent)
    assert workspace.rows[0].components[1].width == 6
    assert workspace.rows[0].components[1].height == 2

    # Case 3: Nested Columns
    rows = [
        WorkspaceRow(components=[
            WorkspaceColumn(components=[WorkspaceRow(components=[plot_component_1]),
                                        WorkspaceRow(components=[plot_component_2])]),
            plot_component_3
        ])
    ]
    workspace = Workspace(rows=rows, alias='testing-something', name='Testing')
    workspace = Workspace.from_dict(workspace.as_dict())

    assert isinstance(workspace.rows[0], WorkspaceRow)
    assert isinstance(workspace.rows[0].components[0], WorkspaceColumn)
    assert workspace.rows[0].components[0].width == 6
    assert len(workspace.rows[0].components[0].components) == 2
    assert workspace.rows[0].components[0].components[0].components[0].height == 1
    assert workspace.rows[0].components[0].components[1].components[0].height == 2
    assert workspace.rows[0].components[1].height == 3


if __name__ == '__main__':
    pytest.main(args=["test_workspace.py"])
