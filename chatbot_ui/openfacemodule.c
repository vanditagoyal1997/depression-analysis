#include <Python.h>
#include<LandmarkDetectorFunc.h>

static PyObject *
conv_gaze_au(PyObject *self)
{
	LandmarkDetector::FaceModelParameters det_parameters;
LandmarkDetector::CLNF face_model(det_parameters.model_location);	

while(video)
{
    bool success = LandmarkDetector::DetectLandmarksInVideo(grayscale_image, face_model, det_parameters);
			
    cv::Point3f gazeDirection0(0, 0, -1);
    cv::Point3f gazeDirection1(0, 0, -1);
	cv::Vec2d gazeAngle(0, 0);

    if (success && det_parameters.track_gaze)
    {
        GazeAnalysis::EstimateGaze(face_model, gazeDirection0, fx, fy, cx, cy, true);
        GazeAnalysis::EstimateGaze(face_model, gazeDirection1, fx, fy, cx, cy, false);
		gazeAngle = GazeAnalysis::GetGazeAngle(gazeDirection0, gazeDirection1, pose_estimate);
    }
}
}